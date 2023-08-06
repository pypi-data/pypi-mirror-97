import json
import os

from datetime import datetime
from functools import reduce
from typing import Dict
from typing import List
from typing import Tuple

from google.rpc.error_details_pb2 import BadRequest
from google.protobuf.json_format import MessageToDict
from google.protobuf.struct_pb2 import Struct
from grpclib.client import Channel
from grpclib.exceptions import GRPCError
from grpclib.events import SendRequest
from grpclib.events import listen


from slyce.exception import ExecuteWorkflowError
from slyce.exception import UploadImageError
from slyce.protobufgen.auth_grpc import AuthStub
from slyce.protobufgen.auth_pb2 import GetAuthTokenRequest
from slyce.protobufgen.common_pb2 import Point
from slyce.protobufgen.image_grpc import ImageStub
from slyce.protobufgen.image_pb2 import UploadImageRequest
from slyce.protobufgen.workflow_grpc import WorkflowStub
from slyce.protobufgen.workflow_pb2 import ExecuteWorkflowRequest


class SlyceClient:
    """ Client for calling Slyce
    """

    def __init__(self, *, credentials: str = None, fingerprint: str = None):
        """
        Args:
            credentials (str, optional): Path to credentials. Defaults os.environ['SLYCE_APPLICATION_CREDENTIALS'].
            fingerprint (str, optional): Unique identifier for the instance of this library.

        Raises:
            ValueError: if missing or invalid credentials.
        """
        try:
            if not credentials:
                with open(os.environ['SLYCE_APPLICATION_CREDENTIALS'], 'r') as f:
                    credentials = json.load(f)

                if not credentials['account_id'] or not credentials['space_id'] or not credentials['api_key']:
                    raise Exception

        except Exception:
            raise ValueError('Missing or invalid credentials.')

        self._account_id = credentials['account_id']
        self._space_id = credentials['space_id']
        self._api_key = credentials['api_key']
        self._fingerprint = fingerprint

        self._auth_token = None
        self._auth_token_expiry = None

        self._channel = Channel('forgex.slyce.it', 443, ssl=True)

        listen(self._channel, SendRequest, self._send_request)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    async def _send_request(self, event):
        try:
            if event.method_name == '/Auth/GetAuthToken':
                return

            if not self._auth_token or self._auth_token_expiry - int(datetime.utcnow().timestamp() * 1000) < 30:
                stub = AuthStub(self._channel)
                async with stub.GetAuthToken.open() as stream:
                    await stream.send_message(GetAuthTokenRequest(
                        api_key=self._api_key,
                        account_id=self._account_id
                    ))
                    res = await stream.recv_message()
                    self._auth_token = res.token
                    self._auth_token_expiry = res.expiry

            event.metadata['auth-token'] = self._auth_token
        except Exception as e:
            print(e)

    def close(self):
        self._channel.close()

    async def _execute_workflow(self,
                                *,
                                workflow_id: str = None,
                                weld_statement: str = None,
                                image_id: str = None,
                                language_code: str = None,
                                country_code: str = None,
                                anchor: Tuple[int, int] = None,
                                roi: List[Tuple[int, int]] = None,
                                options: Dict = None,
                                **_) -> Dict:
        try:
            workflow_options = Struct()
            workflow_options.update(options or {})

            request = ExecuteWorkflowRequest(
                account_id=self._account_id,
                space_id=self._space_id,
                image_id=image_id,
                fingerprint=self._fingerprint,
                language_code=language_code,
                country_code=country_code,
                workflow_options=workflow_options,
                anchor=Point(x=anchor[0], y=anchor[1]) if anchor else None,
                roi=[Point(x=p[0], y=p[1]) for p in roi] if roi else None
            )

            if workflow_id:
                request.workflow_id = workflow_id
            elif weld_statement:
                request.weld_statement = weld_statement

            stub = WorkflowStub(self._channel)

            res = await stub.ExecuteWorkflow(request)

            if res.errors:
                raise ExecuteWorkflowError(res.errors)

            data = MessageToDict(getattr(res, res.WhichOneof('data')), preserving_proto_field_name=True)
            data['results'] = data.get('results')
            return_value = MessageToDict(res, preserving_proto_field_name=True)
            return_value.pop('search_data', None)
            return_value.pop('classifier_data', None)
            return_value['data'] = data
            return return_value

        except GRPCError as e:
            if not e.details:
                raise Exception

            details = reduce(
                lambda res, detail: {
                    **res,
                    **{v.field: v.description for v in detail.field_violations}
                },
                [detail for detail in e.details if isinstance(detail, BadRequest)],
                {}
            )

            raise ExecuteWorkflowError(details)

        except ExecuteWorkflowError as e:
            raise e
        except Exception:
            raise ExecuteWorkflowError('An unknown error occured.')

    async def execute_workflow(self,
                               workflow_id: str,
                               *,
                               image_id: str = None,
                               language_code: str = None,
                               country_code: str = None,
                               anchor: Tuple[int, int] = None,
                               roi: List[Tuple[int, int]] = None,
                               options: Dict = None,
                               **_) -> Dict:

        """Execute a workflow.

        Args:
            workflow_id(str): ID of the workflow.
            image_id(str, optional): ID of the image to use in the workflow.
            language_code(str, optional): Language code to use in the workflow.
            country_code(str, optional): Country code to use in the workflow.
            anchor(Tuple[int, int], optional): Anchor point in reference to image.
            roi(List[Tuple[int, int]], optional): Region of interest, as points, in reference to image.
            options(Dict, optional): Any options to be passed into the workflow at runtime.

        Raises:
            ExecuteWorkflowError

        Returns:
            Dict: Workflow Execution Response object.
        """

        return await self._execute_workflow(
            workflow_id=workflow_id,
            image_id=image_id,
            language_code=language_code,
            country_code=country_code,
            anchor=anchor,
            roi=roi,
            options=options
        )

    async def execute_weld(self,
                           weld_statement: str,
                           *,
                           image_id: str = None,
                           language_code: str = None,
                           country_code: str = None,
                           anchor: Tuple[int, int] = None,
                           roi: List[Tuple[int, int]] = None,
                           options: Dict = None,
                           **_) -> Dict:

        """Execute WELD.

        Args:
            weld_statement(str): WELD statement to execute.
            image_id(str, optional): ID of the image to use in the workflow.
            language_code(str, optional): Language code to use in the workflow.
            country_code(str, optional): Country code to use in the workflow.
            anchor(Tuple[int, int], optional): Anchor point in reference to image.
            roi(List[Tuple[int, int]], optional): Region of interest, as points, in reference to image.
            options(Dict, optional): Any options to be passed into the workflow at runtime.

        Raises:
            ExecuteWorkflowError

        Returns:
            Dict: Workflow Execution Response object.
        """

        return await self._execute_workflow(
            weld_statement=weld_statement,
            image_id=image_id,
            language_code=language_code,
            country_code=country_code,
            anchor=anchor,
            roi=roi,
            options=options
        )

    async def execute_weld_from_file(self,
                                     weld_filepath: str,
                                     *,
                                     image_id: str = None,
                                     language_code: str = None,
                                     country_code: str = None,
                                     anchor: Tuple[int, int] = None,
                                     roi: List[Tuple[int, int]] = None,
                                     options: Dict = None,
                                     **_) -> Dict:

        """Execute WELD from a file.

        Args:
            weld_filepath(str): Filepath containing WELD statement.
            image_id(str, optional): ID of the image to use in the workflow.
            language_code(str, optional): Language code to use in the workflow.
            country_code(str, optional): Country code to use in the workflow.
            anchor(Tuple[int, int], optional): Anchor point in reference to image.
            roi(List[Tuple[int, int]], optional): Region of interest, as points, in reference to image.
            options(Dict, optional): Any options to be passed into the workflow at runtime.

        Raises:
            ExecuteWorkflowError

        Returns:
            Dict: Workflow Execution Response object.
        """

        weld_statement = None
        try:
            with open(weld_filepath, 'r') as f:
                weld_statement = f.read()
        except FileNotFoundError as e:
            raise ExecuteWorkflowError(str(e))

        return await self._execute_workflow(
            weld_statement=weld_statement,
            image_id=image_id,
            language_code=language_code,
            country_code=country_code,
            anchor=anchor,
            roi=roi,
            options=options
        )

    async def upload_image(self, filepath: str = None, url: str = None) -> str:
        """Upload an image.

        Args:
            filepath (str): Path to the image file.
            url (str): URL of ther image file.
        Raises:
            ValueError
            FileNotFoundError
            UploadImageError
        Returns:
            str: The ID of the uploaded image.
        """
        if not filepath and not url:
            raise ValueError("A 'filepath' or 'url' must be specified.")

        try:
            stub = ImageStub(self._channel)
            async with stub.UploadImage.open() as stream:
                if url:
                    await stream.send_message(UploadImageRequest(
                        account_id=self._account_id,
                        fingerprint=self._fingerprint,
                        url=url
                    ))
                else:
                    f = open(filepath, 'rb') if isinstance(filepath, str) else filepath
                    try:
                        while True:
                            data = f.read(1024 * 1024)

                            if not data:
                                break

                            await stream.send_message(UploadImageRequest(
                                account_id=self._account_id,
                                fingerprint=self._fingerprint,
                                data=data
                            ))
                    finally:
                        try:
                            f.close()
                        except Exception:
                            pass

                await stream.end()
                res = await stream.recv_message()
                return res.id
        except Exception as e:
            raise e
            if isinstance(e, UploadImageError):
                raise e
            if isinstance(e, FileNotFoundError):
                raise e
            raise UploadImageError('An unknown error occured.')
