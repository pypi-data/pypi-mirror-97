# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_ocr20191230 import models as ocr_20191230_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_rpc import models as rpc_models
from alibabacloud_openplatform20191219.client import Client as OpenPlatformClient
from alibabacloud_openplatform20191219 import models as open_platform_models
from alibabacloud_oss_sdk import models as oss_models
from alibabacloud_tea_fileform import models as file_form_models
from alibabacloud_oss_util import models as ossutil_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient
from alibabacloud_oss_sdk.client import Client as OSSClient


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = 'regional'
        self.check_config(config)
        self._endpoint = self.get_endpoint('ocr', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def recognize_driving_license_with_options(
        self,
        request: ocr_20191230_models.RecognizeDrivingLicenseRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeDrivingLicenseResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeDrivingLicenseResponse().from_map(
            self.do_rpcrequest('RecognizeDrivingLicense', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_driving_license_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeDrivingLicenseRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeDrivingLicenseResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeDrivingLicenseResponse().from_map(
            await self.do_rpcrequest_async('RecognizeDrivingLicense', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_driving_license(
        self,
        request: ocr_20191230_models.RecognizeDrivingLicenseRequest,
    ) -> ocr_20191230_models.RecognizeDrivingLicenseResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_driving_license_with_options(request, runtime)

    async def recognize_driving_license_async(
        self,
        request: ocr_20191230_models.RecognizeDrivingLicenseRequest,
    ) -> ocr_20191230_models.RecognizeDrivingLicenseResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_driving_license_with_options_async(request, runtime)

    def recognize_driving_license_advance(
        self,
        request: ocr_20191230_models.RecognizeDrivingLicenseAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeDrivingLicenseResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_driving_license_req = ocr_20191230_models.RecognizeDrivingLicenseRequest()
        OpenApiUtilClient.convert(request, recognize_driving_license_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_driving_license_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_driving_license_resp = self.recognize_driving_license_with_options(recognize_driving_license_req, runtime)
        return recognize_driving_license_resp

    async def recognize_driving_license_advance_async(
        self,
        request: ocr_20191230_models.RecognizeDrivingLicenseAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeDrivingLicenseResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_driving_license_req = ocr_20191230_models.RecognizeDrivingLicenseRequest()
        OpenApiUtilClient.convert(request, recognize_driving_license_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_driving_license_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_driving_license_resp = await self.recognize_driving_license_with_options_async(recognize_driving_license_req, runtime)
        return recognize_driving_license_resp

    def recognize_chinapassport_with_options(
        self,
        request: ocr_20191230_models.RecognizeChinapassportRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeChinapassportResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeChinapassportResponse().from_map(
            self.do_rpcrequest('RecognizeChinapassport', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_chinapassport_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeChinapassportRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeChinapassportResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeChinapassportResponse().from_map(
            await self.do_rpcrequest_async('RecognizeChinapassport', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_chinapassport(
        self,
        request: ocr_20191230_models.RecognizeChinapassportRequest,
    ) -> ocr_20191230_models.RecognizeChinapassportResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_chinapassport_with_options(request, runtime)

    async def recognize_chinapassport_async(
        self,
        request: ocr_20191230_models.RecognizeChinapassportRequest,
    ) -> ocr_20191230_models.RecognizeChinapassportResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_chinapassport_with_options_async(request, runtime)

    def recognize_chinapassport_advance(
        self,
        request: ocr_20191230_models.RecognizeChinapassportAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeChinapassportResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_chinapassport_req = ocr_20191230_models.RecognizeChinapassportRequest()
        OpenApiUtilClient.convert(request, recognize_chinapassport_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_chinapassport_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_chinapassport_resp = self.recognize_chinapassport_with_options(recognize_chinapassport_req, runtime)
        return recognize_chinapassport_resp

    async def recognize_chinapassport_advance_async(
        self,
        request: ocr_20191230_models.RecognizeChinapassportAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeChinapassportResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_chinapassport_req = ocr_20191230_models.RecognizeChinapassportRequest()
        OpenApiUtilClient.convert(request, recognize_chinapassport_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_chinapassport_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_chinapassport_resp = await self.recognize_chinapassport_with_options_async(recognize_chinapassport_req, runtime)
        return recognize_chinapassport_resp

    def trim_document_with_options(
        self,
        request: ocr_20191230_models.TrimDocumentRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.TrimDocumentResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.TrimDocumentResponse().from_map(
            self.do_rpcrequest('TrimDocument', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def trim_document_with_options_async(
        self,
        request: ocr_20191230_models.TrimDocumentRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.TrimDocumentResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.TrimDocumentResponse().from_map(
            await self.do_rpcrequest_async('TrimDocument', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def trim_document(
        self,
        request: ocr_20191230_models.TrimDocumentRequest,
    ) -> ocr_20191230_models.TrimDocumentResponse:
        runtime = util_models.RuntimeOptions()
        return self.trim_document_with_options(request, runtime)

    async def trim_document_async(
        self,
        request: ocr_20191230_models.TrimDocumentRequest,
    ) -> ocr_20191230_models.TrimDocumentResponse:
        runtime = util_models.RuntimeOptions()
        return await self.trim_document_with_options_async(request, runtime)

    def trim_document_advance(
        self,
        request: ocr_20191230_models.TrimDocumentAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.TrimDocumentResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        trim_document_req = ocr_20191230_models.TrimDocumentRequest()
        OpenApiUtilClient.convert(request, trim_document_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.file_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        trim_document_req.file_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        trim_document_resp = self.trim_document_with_options(trim_document_req, runtime)
        return trim_document_resp

    async def trim_document_advance_async(
        self,
        request: ocr_20191230_models.TrimDocumentAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.TrimDocumentResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        trim_document_req = ocr_20191230_models.TrimDocumentRequest()
        OpenApiUtilClient.convert(request, trim_document_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.file_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        trim_document_req.file_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        trim_document_resp = await self.trim_document_with_options_async(trim_document_req, runtime)
        return trim_document_resp

    def recognize_table_with_options(
        self,
        request: ocr_20191230_models.RecognizeTableRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTableResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeTableResponse().from_map(
            self.do_rpcrequest('RecognizeTable', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_table_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeTableRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTableResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeTableResponse().from_map(
            await self.do_rpcrequest_async('RecognizeTable', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_table(
        self,
        request: ocr_20191230_models.RecognizeTableRequest,
    ) -> ocr_20191230_models.RecognizeTableResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_table_with_options(request, runtime)

    async def recognize_table_async(
        self,
        request: ocr_20191230_models.RecognizeTableRequest,
    ) -> ocr_20191230_models.RecognizeTableResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_table_with_options_async(request, runtime)

    def recognize_table_advance(
        self,
        request: ocr_20191230_models.RecognizeTableAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTableResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_table_req = ocr_20191230_models.RecognizeTableRequest()
        OpenApiUtilClient.convert(request, recognize_table_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_table_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_table_resp = self.recognize_table_with_options(recognize_table_req, runtime)
        return recognize_table_resp

    async def recognize_table_advance_async(
        self,
        request: ocr_20191230_models.RecognizeTableAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTableResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_table_req = ocr_20191230_models.RecognizeTableRequest()
        OpenApiUtilClient.convert(request, recognize_table_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_table_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_table_resp = await self.recognize_table_with_options_async(recognize_table_req, runtime)
        return recognize_table_resp

    def recognize_identity_card_with_options(
        self,
        request: ocr_20191230_models.RecognizeIdentityCardRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeIdentityCardResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeIdentityCardResponse().from_map(
            self.do_rpcrequest('RecognizeIdentityCard', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_identity_card_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeIdentityCardRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeIdentityCardResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeIdentityCardResponse().from_map(
            await self.do_rpcrequest_async('RecognizeIdentityCard', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_identity_card(
        self,
        request: ocr_20191230_models.RecognizeIdentityCardRequest,
    ) -> ocr_20191230_models.RecognizeIdentityCardResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_identity_card_with_options(request, runtime)

    async def recognize_identity_card_async(
        self,
        request: ocr_20191230_models.RecognizeIdentityCardRequest,
    ) -> ocr_20191230_models.RecognizeIdentityCardResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_identity_card_with_options_async(request, runtime)

    def recognize_identity_card_advance(
        self,
        request: ocr_20191230_models.RecognizeIdentityCardAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeIdentityCardResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_identity_card_req = ocr_20191230_models.RecognizeIdentityCardRequest()
        OpenApiUtilClient.convert(request, recognize_identity_card_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_identity_card_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_identity_card_resp = self.recognize_identity_card_with_options(recognize_identity_card_req, runtime)
        return recognize_identity_card_resp

    async def recognize_identity_card_advance_async(
        self,
        request: ocr_20191230_models.RecognizeIdentityCardAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeIdentityCardResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_identity_card_req = ocr_20191230_models.RecognizeIdentityCardRequest()
        OpenApiUtilClient.convert(request, recognize_identity_card_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_identity_card_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_identity_card_resp = await self.recognize_identity_card_with_options_async(recognize_identity_card_req, runtime)
        return recognize_identity_card_resp

    def recognize_business_license_with_options(
        self,
        request: ocr_20191230_models.RecognizeBusinessLicenseRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeBusinessLicenseResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeBusinessLicenseResponse().from_map(
            self.do_rpcrequest('RecognizeBusinessLicense', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_business_license_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeBusinessLicenseRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeBusinessLicenseResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeBusinessLicenseResponse().from_map(
            await self.do_rpcrequest_async('RecognizeBusinessLicense', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_business_license(
        self,
        request: ocr_20191230_models.RecognizeBusinessLicenseRequest,
    ) -> ocr_20191230_models.RecognizeBusinessLicenseResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_business_license_with_options(request, runtime)

    async def recognize_business_license_async(
        self,
        request: ocr_20191230_models.RecognizeBusinessLicenseRequest,
    ) -> ocr_20191230_models.RecognizeBusinessLicenseResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_business_license_with_options_async(request, runtime)

    def recognize_business_license_advance(
        self,
        request: ocr_20191230_models.RecognizeBusinessLicenseAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeBusinessLicenseResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_business_license_req = ocr_20191230_models.RecognizeBusinessLicenseRequest()
        OpenApiUtilClient.convert(request, recognize_business_license_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_business_license_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_business_license_resp = self.recognize_business_license_with_options(recognize_business_license_req, runtime)
        return recognize_business_license_resp

    async def recognize_business_license_advance_async(
        self,
        request: ocr_20191230_models.RecognizeBusinessLicenseAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeBusinessLicenseResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_business_license_req = ocr_20191230_models.RecognizeBusinessLicenseRequest()
        OpenApiUtilClient.convert(request, recognize_business_license_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_business_license_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_business_license_resp = await self.recognize_business_license_with_options_async(recognize_business_license_req, runtime)
        return recognize_business_license_resp

    def recognize_bank_card_with_options(
        self,
        request: ocr_20191230_models.RecognizeBankCardRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeBankCardResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeBankCardResponse().from_map(
            self.do_rpcrequest('RecognizeBankCard', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_bank_card_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeBankCardRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeBankCardResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeBankCardResponse().from_map(
            await self.do_rpcrequest_async('RecognizeBankCard', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_bank_card(
        self,
        request: ocr_20191230_models.RecognizeBankCardRequest,
    ) -> ocr_20191230_models.RecognizeBankCardResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_bank_card_with_options(request, runtime)

    async def recognize_bank_card_async(
        self,
        request: ocr_20191230_models.RecognizeBankCardRequest,
    ) -> ocr_20191230_models.RecognizeBankCardResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_bank_card_with_options_async(request, runtime)

    def recognize_bank_card_advance(
        self,
        request: ocr_20191230_models.RecognizeBankCardAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeBankCardResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_bank_card_req = ocr_20191230_models.RecognizeBankCardRequest()
        OpenApiUtilClient.convert(request, recognize_bank_card_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_bank_card_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_bank_card_resp = self.recognize_bank_card_with_options(recognize_bank_card_req, runtime)
        return recognize_bank_card_resp

    async def recognize_bank_card_advance_async(
        self,
        request: ocr_20191230_models.RecognizeBankCardAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeBankCardResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_bank_card_req = ocr_20191230_models.RecognizeBankCardRequest()
        OpenApiUtilClient.convert(request, recognize_bank_card_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_bank_card_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_bank_card_resp = await self.recognize_bank_card_with_options_async(recognize_bank_card_req, runtime)
        return recognize_bank_card_resp

    def recognize_verificationcode_with_options(
        self,
        request: ocr_20191230_models.RecognizeVerificationcodeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeVerificationcodeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeVerificationcodeResponse().from_map(
            self.do_rpcrequest('RecognizeVerificationcode', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_verificationcode_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeVerificationcodeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeVerificationcodeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeVerificationcodeResponse().from_map(
            await self.do_rpcrequest_async('RecognizeVerificationcode', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_verificationcode(
        self,
        request: ocr_20191230_models.RecognizeVerificationcodeRequest,
    ) -> ocr_20191230_models.RecognizeVerificationcodeResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_verificationcode_with_options(request, runtime)

    async def recognize_verificationcode_async(
        self,
        request: ocr_20191230_models.RecognizeVerificationcodeRequest,
    ) -> ocr_20191230_models.RecognizeVerificationcodeResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_verificationcode_with_options_async(request, runtime)

    def recognize_verificationcode_advance(
        self,
        request: ocr_20191230_models.RecognizeVerificationcodeAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeVerificationcodeResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_verificationcode_req = ocr_20191230_models.RecognizeVerificationcodeRequest()
        OpenApiUtilClient.convert(request, recognize_verificationcode_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_verificationcode_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_verificationcode_resp = self.recognize_verificationcode_with_options(recognize_verificationcode_req, runtime)
        return recognize_verificationcode_resp

    async def recognize_verificationcode_advance_async(
        self,
        request: ocr_20191230_models.RecognizeVerificationcodeAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeVerificationcodeResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_verificationcode_req = ocr_20191230_models.RecognizeVerificationcodeRequest()
        OpenApiUtilClient.convert(request, recognize_verificationcode_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_verificationcode_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_verificationcode_resp = await self.recognize_verificationcode_with_options_async(recognize_verificationcode_req, runtime)
        return recognize_verificationcode_resp

    def recognize_account_page_with_options(
        self,
        request: ocr_20191230_models.RecognizeAccountPageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeAccountPageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeAccountPageResponse().from_map(
            self.do_rpcrequest('RecognizeAccountPage', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_account_page_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeAccountPageRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeAccountPageResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeAccountPageResponse().from_map(
            await self.do_rpcrequest_async('RecognizeAccountPage', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_account_page(
        self,
        request: ocr_20191230_models.RecognizeAccountPageRequest,
    ) -> ocr_20191230_models.RecognizeAccountPageResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_account_page_with_options(request, runtime)

    async def recognize_account_page_async(
        self,
        request: ocr_20191230_models.RecognizeAccountPageRequest,
    ) -> ocr_20191230_models.RecognizeAccountPageResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_account_page_with_options_async(request, runtime)

    def recognize_account_page_advance(
        self,
        request: ocr_20191230_models.RecognizeAccountPageAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeAccountPageResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_account_page_req = ocr_20191230_models.RecognizeAccountPageRequest()
        OpenApiUtilClient.convert(request, recognize_account_page_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_account_page_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_account_page_resp = self.recognize_account_page_with_options(recognize_account_page_req, runtime)
        return recognize_account_page_resp

    async def recognize_account_page_advance_async(
        self,
        request: ocr_20191230_models.RecognizeAccountPageAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeAccountPageResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_account_page_req = ocr_20191230_models.RecognizeAccountPageRequest()
        OpenApiUtilClient.convert(request, recognize_account_page_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_account_page_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_account_page_resp = await self.recognize_account_page_with_options_async(recognize_account_page_req, runtime)
        return recognize_account_page_resp

    def recognize_character_with_options(
        self,
        request: ocr_20191230_models.RecognizeCharacterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeCharacterResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeCharacterResponse().from_map(
            self.do_rpcrequest('RecognizeCharacter', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_character_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeCharacterRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeCharacterResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeCharacterResponse().from_map(
            await self.do_rpcrequest_async('RecognizeCharacter', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_character(
        self,
        request: ocr_20191230_models.RecognizeCharacterRequest,
    ) -> ocr_20191230_models.RecognizeCharacterResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_character_with_options(request, runtime)

    async def recognize_character_async(
        self,
        request: ocr_20191230_models.RecognizeCharacterRequest,
    ) -> ocr_20191230_models.RecognizeCharacterResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_character_with_options_async(request, runtime)

    def recognize_character_advance(
        self,
        request: ocr_20191230_models.RecognizeCharacterAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeCharacterResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_character_req = ocr_20191230_models.RecognizeCharacterRequest()
        OpenApiUtilClient.convert(request, recognize_character_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_character_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_character_resp = self.recognize_character_with_options(recognize_character_req, runtime)
        return recognize_character_resp

    async def recognize_character_advance_async(
        self,
        request: ocr_20191230_models.RecognizeCharacterAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeCharacterResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_character_req = ocr_20191230_models.RecognizeCharacterRequest()
        OpenApiUtilClient.convert(request, recognize_character_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_character_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_character_resp = await self.recognize_character_with_options_async(recognize_character_req, runtime)
        return recognize_character_resp

    def get_async_job_result_with_options(
        self,
        request: ocr_20191230_models.GetAsyncJobResultRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.GetAsyncJobResultResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.GetAsyncJobResultResponse().from_map(
            self.do_rpcrequest('GetAsyncJobResult', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def get_async_job_result_with_options_async(
        self,
        request: ocr_20191230_models.GetAsyncJobResultRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.GetAsyncJobResultResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.GetAsyncJobResultResponse().from_map(
            await self.do_rpcrequest_async('GetAsyncJobResult', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def get_async_job_result(
        self,
        request: ocr_20191230_models.GetAsyncJobResultRequest,
    ) -> ocr_20191230_models.GetAsyncJobResultResponse:
        runtime = util_models.RuntimeOptions()
        return self.get_async_job_result_with_options(request, runtime)

    async def get_async_job_result_async(
        self,
        request: ocr_20191230_models.GetAsyncJobResultRequest,
    ) -> ocr_20191230_models.GetAsyncJobResultResponse:
        runtime = util_models.RuntimeOptions()
        return await self.get_async_job_result_with_options_async(request, runtime)

    def recognize_takeout_order_with_options(
        self,
        request: ocr_20191230_models.RecognizeTakeoutOrderRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTakeoutOrderResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeTakeoutOrderResponse().from_map(
            self.do_rpcrequest('RecognizeTakeoutOrder', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_takeout_order_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeTakeoutOrderRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTakeoutOrderResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeTakeoutOrderResponse().from_map(
            await self.do_rpcrequest_async('RecognizeTakeoutOrder', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_takeout_order(
        self,
        request: ocr_20191230_models.RecognizeTakeoutOrderRequest,
    ) -> ocr_20191230_models.RecognizeTakeoutOrderResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_takeout_order_with_options(request, runtime)

    async def recognize_takeout_order_async(
        self,
        request: ocr_20191230_models.RecognizeTakeoutOrderRequest,
    ) -> ocr_20191230_models.RecognizeTakeoutOrderResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_takeout_order_with_options_async(request, runtime)

    def recognize_takeout_order_advance(
        self,
        request: ocr_20191230_models.RecognizeTakeoutOrderAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTakeoutOrderResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_takeout_order_req = ocr_20191230_models.RecognizeTakeoutOrderRequest()
        OpenApiUtilClient.convert(request, recognize_takeout_order_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_takeout_order_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_takeout_order_resp = self.recognize_takeout_order_with_options(recognize_takeout_order_req, runtime)
        return recognize_takeout_order_resp

    async def recognize_takeout_order_advance_async(
        self,
        request: ocr_20191230_models.RecognizeTakeoutOrderAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTakeoutOrderResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_takeout_order_req = ocr_20191230_models.RecognizeTakeoutOrderRequest()
        OpenApiUtilClient.convert(request, recognize_takeout_order_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_takeout_order_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_takeout_order_resp = await self.recognize_takeout_order_with_options_async(recognize_takeout_order_req, runtime)
        return recognize_takeout_order_resp

    def recognize_business_card_with_options(
        self,
        request: ocr_20191230_models.RecognizeBusinessCardRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeBusinessCardResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeBusinessCardResponse().from_map(
            self.do_rpcrequest('RecognizeBusinessCard', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_business_card_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeBusinessCardRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeBusinessCardResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeBusinessCardResponse().from_map(
            await self.do_rpcrequest_async('RecognizeBusinessCard', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_business_card(
        self,
        request: ocr_20191230_models.RecognizeBusinessCardRequest,
    ) -> ocr_20191230_models.RecognizeBusinessCardResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_business_card_with_options(request, runtime)

    async def recognize_business_card_async(
        self,
        request: ocr_20191230_models.RecognizeBusinessCardRequest,
    ) -> ocr_20191230_models.RecognizeBusinessCardResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_business_card_with_options_async(request, runtime)

    def recognize_business_card_advance(
        self,
        request: ocr_20191230_models.RecognizeBusinessCardAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeBusinessCardResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_business_card_req = ocr_20191230_models.RecognizeBusinessCardRequest()
        OpenApiUtilClient.convert(request, recognize_business_card_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_business_card_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_business_card_resp = self.recognize_business_card_with_options(recognize_business_card_req, runtime)
        return recognize_business_card_resp

    async def recognize_business_card_advance_async(
        self,
        request: ocr_20191230_models.RecognizeBusinessCardAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeBusinessCardResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_business_card_req = ocr_20191230_models.RecognizeBusinessCardRequest()
        OpenApiUtilClient.convert(request, recognize_business_card_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_business_card_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_business_card_resp = await self.recognize_business_card_with_options_async(recognize_business_card_req, runtime)
        return recognize_business_card_resp

    def detect_card_screenshot_with_options(
        self,
        request: ocr_20191230_models.DetectCardScreenshotRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.DetectCardScreenshotResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.DetectCardScreenshotResponse().from_map(
            self.do_rpcrequest('DetectCardScreenshot', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def detect_card_screenshot_with_options_async(
        self,
        request: ocr_20191230_models.DetectCardScreenshotRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.DetectCardScreenshotResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.DetectCardScreenshotResponse().from_map(
            await self.do_rpcrequest_async('DetectCardScreenshot', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def detect_card_screenshot(
        self,
        request: ocr_20191230_models.DetectCardScreenshotRequest,
    ) -> ocr_20191230_models.DetectCardScreenshotResponse:
        runtime = util_models.RuntimeOptions()
        return self.detect_card_screenshot_with_options(request, runtime)

    async def detect_card_screenshot_async(
        self,
        request: ocr_20191230_models.DetectCardScreenshotRequest,
    ) -> ocr_20191230_models.DetectCardScreenshotResponse:
        runtime = util_models.RuntimeOptions()
        return await self.detect_card_screenshot_with_options_async(request, runtime)

    def detect_card_screenshot_advance(
        self,
        request: ocr_20191230_models.DetectCardScreenshotAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.DetectCardScreenshotResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        detect_card_screenshot_req = ocr_20191230_models.DetectCardScreenshotRequest()
        OpenApiUtilClient.convert(request, detect_card_screenshot_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        detect_card_screenshot_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        detect_card_screenshot_resp = self.detect_card_screenshot_with_options(detect_card_screenshot_req, runtime)
        return detect_card_screenshot_resp

    async def detect_card_screenshot_advance_async(
        self,
        request: ocr_20191230_models.DetectCardScreenshotAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.DetectCardScreenshotResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        detect_card_screenshot_req = ocr_20191230_models.DetectCardScreenshotRequest()
        OpenApiUtilClient.convert(request, detect_card_screenshot_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        detect_card_screenshot_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        detect_card_screenshot_resp = await self.detect_card_screenshot_with_options_async(detect_card_screenshot_req, runtime)
        return detect_card_screenshot_resp

    def recognize_driver_license_with_options(
        self,
        request: ocr_20191230_models.RecognizeDriverLicenseRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeDriverLicenseResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeDriverLicenseResponse().from_map(
            self.do_rpcrequest('RecognizeDriverLicense', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_driver_license_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeDriverLicenseRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeDriverLicenseResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeDriverLicenseResponse().from_map(
            await self.do_rpcrequest_async('RecognizeDriverLicense', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_driver_license(
        self,
        request: ocr_20191230_models.RecognizeDriverLicenseRequest,
    ) -> ocr_20191230_models.RecognizeDriverLicenseResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_driver_license_with_options(request, runtime)

    async def recognize_driver_license_async(
        self,
        request: ocr_20191230_models.RecognizeDriverLicenseRequest,
    ) -> ocr_20191230_models.RecognizeDriverLicenseResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_driver_license_with_options_async(request, runtime)

    def recognize_driver_license_advance(
        self,
        request: ocr_20191230_models.RecognizeDriverLicenseAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeDriverLicenseResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_driver_license_req = ocr_20191230_models.RecognizeDriverLicenseRequest()
        OpenApiUtilClient.convert(request, recognize_driver_license_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_driver_license_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_driver_license_resp = self.recognize_driver_license_with_options(recognize_driver_license_req, runtime)
        return recognize_driver_license_resp

    async def recognize_driver_license_advance_async(
        self,
        request: ocr_20191230_models.RecognizeDriverLicenseAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeDriverLicenseResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_driver_license_req = ocr_20191230_models.RecognizeDriverLicenseRequest()
        OpenApiUtilClient.convert(request, recognize_driver_license_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_driver_license_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_driver_license_resp = await self.recognize_driver_license_with_options_async(recognize_driver_license_req, runtime)
        return recognize_driver_license_resp

    def recognize_license_plate_with_options(
        self,
        request: ocr_20191230_models.RecognizeLicensePlateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeLicensePlateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeLicensePlateResponse().from_map(
            self.do_rpcrequest('RecognizeLicensePlate', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_license_plate_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeLicensePlateRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeLicensePlateResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeLicensePlateResponse().from_map(
            await self.do_rpcrequest_async('RecognizeLicensePlate', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_license_plate(
        self,
        request: ocr_20191230_models.RecognizeLicensePlateRequest,
    ) -> ocr_20191230_models.RecognizeLicensePlateResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_license_plate_with_options(request, runtime)

    async def recognize_license_plate_async(
        self,
        request: ocr_20191230_models.RecognizeLicensePlateRequest,
    ) -> ocr_20191230_models.RecognizeLicensePlateResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_license_plate_with_options_async(request, runtime)

    def recognize_license_plate_advance(
        self,
        request: ocr_20191230_models.RecognizeLicensePlateAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeLicensePlateResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_license_plate_req = ocr_20191230_models.RecognizeLicensePlateRequest()
        OpenApiUtilClient.convert(request, recognize_license_plate_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_license_plate_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_license_plate_resp = self.recognize_license_plate_with_options(recognize_license_plate_req, runtime)
        return recognize_license_plate_resp

    async def recognize_license_plate_advance_async(
        self,
        request: ocr_20191230_models.RecognizeLicensePlateAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeLicensePlateResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_license_plate_req = ocr_20191230_models.RecognizeLicensePlateRequest()
        OpenApiUtilClient.convert(request, recognize_license_plate_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_license_plate_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_license_plate_resp = await self.recognize_license_plate_with_options_async(recognize_license_plate_req, runtime)
        return recognize_license_plate_resp

    def recognize_stamp_with_options(
        self,
        request: ocr_20191230_models.RecognizeStampRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeStampResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeStampResponse().from_map(
            self.do_rpcrequest('RecognizeStamp', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_stamp_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeStampRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeStampResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeStampResponse().from_map(
            await self.do_rpcrequest_async('RecognizeStamp', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_stamp(
        self,
        request: ocr_20191230_models.RecognizeStampRequest,
    ) -> ocr_20191230_models.RecognizeStampResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_stamp_with_options(request, runtime)

    async def recognize_stamp_async(
        self,
        request: ocr_20191230_models.RecognizeStampRequest,
    ) -> ocr_20191230_models.RecognizeStampResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_stamp_with_options_async(request, runtime)

    def recognize_stamp_advance(
        self,
        request: ocr_20191230_models.RecognizeStampAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeStampResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_stamp_req = ocr_20191230_models.RecognizeStampRequest()
        OpenApiUtilClient.convert(request, recognize_stamp_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_stamp_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_stamp_resp = self.recognize_stamp_with_options(recognize_stamp_req, runtime)
        return recognize_stamp_resp

    async def recognize_stamp_advance_async(
        self,
        request: ocr_20191230_models.RecognizeStampAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeStampResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_stamp_req = ocr_20191230_models.RecognizeStampRequest()
        OpenApiUtilClient.convert(request, recognize_stamp_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_stamp_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_stamp_resp = await self.recognize_stamp_with_options_async(recognize_stamp_req, runtime)
        return recognize_stamp_resp

    def recognize_taxi_invoice_with_options(
        self,
        request: ocr_20191230_models.RecognizeTaxiInvoiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTaxiInvoiceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeTaxiInvoiceResponse().from_map(
            self.do_rpcrequest('RecognizeTaxiInvoice', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_taxi_invoice_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeTaxiInvoiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTaxiInvoiceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeTaxiInvoiceResponse().from_map(
            await self.do_rpcrequest_async('RecognizeTaxiInvoice', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_taxi_invoice(
        self,
        request: ocr_20191230_models.RecognizeTaxiInvoiceRequest,
    ) -> ocr_20191230_models.RecognizeTaxiInvoiceResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_taxi_invoice_with_options(request, runtime)

    async def recognize_taxi_invoice_async(
        self,
        request: ocr_20191230_models.RecognizeTaxiInvoiceRequest,
    ) -> ocr_20191230_models.RecognizeTaxiInvoiceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_taxi_invoice_with_options_async(request, runtime)

    def recognize_taxi_invoice_advance(
        self,
        request: ocr_20191230_models.RecognizeTaxiInvoiceAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTaxiInvoiceResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_taxi_invoice_req = ocr_20191230_models.RecognizeTaxiInvoiceRequest()
        OpenApiUtilClient.convert(request, recognize_taxi_invoice_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_taxi_invoice_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_taxi_invoice_resp = self.recognize_taxi_invoice_with_options(recognize_taxi_invoice_req, runtime)
        return recognize_taxi_invoice_resp

    async def recognize_taxi_invoice_advance_async(
        self,
        request: ocr_20191230_models.RecognizeTaxiInvoiceAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTaxiInvoiceResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_taxi_invoice_req = ocr_20191230_models.RecognizeTaxiInvoiceRequest()
        OpenApiUtilClient.convert(request, recognize_taxi_invoice_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_taxi_invoice_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_taxi_invoice_resp = await self.recognize_taxi_invoice_with_options_async(recognize_taxi_invoice_req, runtime)
        return recognize_taxi_invoice_resp

    def recognize_vatinvoice_with_options(
        self,
        request: ocr_20191230_models.RecognizeVATInvoiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeVATInvoiceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeVATInvoiceResponse().from_map(
            self.do_rpcrequest('RecognizeVATInvoice', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_vatinvoice_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeVATInvoiceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeVATInvoiceResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeVATInvoiceResponse().from_map(
            await self.do_rpcrequest_async('RecognizeVATInvoice', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_vatinvoice(
        self,
        request: ocr_20191230_models.RecognizeVATInvoiceRequest,
    ) -> ocr_20191230_models.RecognizeVATInvoiceResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_vatinvoice_with_options(request, runtime)

    async def recognize_vatinvoice_async(
        self,
        request: ocr_20191230_models.RecognizeVATInvoiceRequest,
    ) -> ocr_20191230_models.RecognizeVATInvoiceResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_vatinvoice_with_options_async(request, runtime)

    def recognize_vatinvoice_advance(
        self,
        request: ocr_20191230_models.RecognizeVATInvoiceAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeVATInvoiceResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_vatinvoice_req = ocr_20191230_models.RecognizeVATInvoiceRequest()
        OpenApiUtilClient.convert(request, recognize_vatinvoice_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.file_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_vatinvoice_req.file_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_vatinvoice_resp = self.recognize_vatinvoice_with_options(recognize_vatinvoice_req, runtime)
        return recognize_vatinvoice_resp

    async def recognize_vatinvoice_advance_async(
        self,
        request: ocr_20191230_models.RecognizeVATInvoiceAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeVATInvoiceResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_vatinvoice_req = ocr_20191230_models.RecognizeVATInvoiceRequest()
        OpenApiUtilClient.convert(request, recognize_vatinvoice_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.file_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_vatinvoice_req.file_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_vatinvoice_resp = await self.recognize_vatinvoice_with_options_async(recognize_vatinvoice_req, runtime)
        return recognize_vatinvoice_resp

    def recognize_passport_mrzwith_options(
        self,
        request: ocr_20191230_models.RecognizePassportMRZRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizePassportMRZResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizePassportMRZResponse().from_map(
            self.do_rpcrequest('RecognizePassportMRZ', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_passport_mrzwith_options_async(
        self,
        request: ocr_20191230_models.RecognizePassportMRZRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizePassportMRZResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizePassportMRZResponse().from_map(
            await self.do_rpcrequest_async('RecognizePassportMRZ', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_passport_mrz(
        self,
        request: ocr_20191230_models.RecognizePassportMRZRequest,
    ) -> ocr_20191230_models.RecognizePassportMRZResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_passport_mrzwith_options(request, runtime)

    async def recognize_passport_mrz_async(
        self,
        request: ocr_20191230_models.RecognizePassportMRZRequest,
    ) -> ocr_20191230_models.RecognizePassportMRZResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_passport_mrzwith_options_async(request, runtime)

    def recognize_passport_mrzadvance(
        self,
        request: ocr_20191230_models.RecognizePassportMRZAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizePassportMRZResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_passport_mrzreq = ocr_20191230_models.RecognizePassportMRZRequest()
        OpenApiUtilClient.convert(request, recognize_passport_mrzreq)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_passport_mrzreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_passport_mrzresp = self.recognize_passport_mrzwith_options(recognize_passport_mrzreq, runtime)
        return recognize_passport_mrzresp

    async def recognize_passport_mrzadvance_async(
        self,
        request: ocr_20191230_models.RecognizePassportMRZAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizePassportMRZResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_passport_mrzreq = ocr_20191230_models.RecognizePassportMRZRequest()
        OpenApiUtilClient.convert(request, recognize_passport_mrzreq)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_passport_mrzreq.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_passport_mrzresp = await self.recognize_passport_mrzwith_options_async(recognize_passport_mrzreq, runtime)
        return recognize_passport_mrzresp

    def recognize_train_ticket_with_options(
        self,
        request: ocr_20191230_models.RecognizeTrainTicketRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTrainTicketResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeTrainTicketResponse().from_map(
            self.do_rpcrequest('RecognizeTrainTicket', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_train_ticket_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeTrainTicketRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTrainTicketResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeTrainTicketResponse().from_map(
            await self.do_rpcrequest_async('RecognizeTrainTicket', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_train_ticket(
        self,
        request: ocr_20191230_models.RecognizeTrainTicketRequest,
    ) -> ocr_20191230_models.RecognizeTrainTicketResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_train_ticket_with_options(request, runtime)

    async def recognize_train_ticket_async(
        self,
        request: ocr_20191230_models.RecognizeTrainTicketRequest,
    ) -> ocr_20191230_models.RecognizeTrainTicketResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_train_ticket_with_options_async(request, runtime)

    def recognize_train_ticket_advance(
        self,
        request: ocr_20191230_models.RecognizeTrainTicketAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTrainTicketResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_train_ticket_req = ocr_20191230_models.RecognizeTrainTicketRequest()
        OpenApiUtilClient.convert(request, recognize_train_ticket_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_train_ticket_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_train_ticket_resp = self.recognize_train_ticket_with_options(recognize_train_ticket_req, runtime)
        return recognize_train_ticket_resp

    async def recognize_train_ticket_advance_async(
        self,
        request: ocr_20191230_models.RecognizeTrainTicketAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeTrainTicketResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_train_ticket_req = ocr_20191230_models.RecognizeTrainTicketRequest()
        OpenApiUtilClient.convert(request, recognize_train_ticket_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_train_ticket_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_train_ticket_resp = await self.recognize_train_ticket_with_options_async(recognize_train_ticket_req, runtime)
        return recognize_train_ticket_resp

    def recognize_poi_name_with_options(
        self,
        request: ocr_20191230_models.RecognizePoiNameRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizePoiNameResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizePoiNameResponse().from_map(
            self.do_rpcrequest('RecognizePoiName', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_poi_name_with_options_async(
        self,
        request: ocr_20191230_models.RecognizePoiNameRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizePoiNameResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizePoiNameResponse().from_map(
            await self.do_rpcrequest_async('RecognizePoiName', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_poi_name(
        self,
        request: ocr_20191230_models.RecognizePoiNameRequest,
    ) -> ocr_20191230_models.RecognizePoiNameResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_poi_name_with_options(request, runtime)

    async def recognize_poi_name_async(
        self,
        request: ocr_20191230_models.RecognizePoiNameRequest,
    ) -> ocr_20191230_models.RecognizePoiNameResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_poi_name_with_options_async(request, runtime)

    def recognize_poi_name_advance(
        self,
        request: ocr_20191230_models.RecognizePoiNameAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizePoiNameResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_poi_name_req = ocr_20191230_models.RecognizePoiNameRequest()
        OpenApiUtilClient.convert(request, recognize_poi_name_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_poi_name_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_poi_name_resp = self.recognize_poi_name_with_options(recognize_poi_name_req, runtime)
        return recognize_poi_name_resp

    async def recognize_poi_name_advance_async(
        self,
        request: ocr_20191230_models.RecognizePoiNameAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizePoiNameResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_poi_name_req = ocr_20191230_models.RecognizePoiNameRequest()
        OpenApiUtilClient.convert(request, recognize_poi_name_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_poi_name_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_poi_name_resp = await self.recognize_poi_name_with_options_async(recognize_poi_name_req, runtime)
        return recognize_poi_name_resp

    def recognize_qr_code_with_options(
        self,
        request: ocr_20191230_models.RecognizeQrCodeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeQrCodeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeQrCodeResponse().from_map(
            self.do_rpcrequest('RecognizeQrCode', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_qr_code_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeQrCodeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeQrCodeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeQrCodeResponse().from_map(
            await self.do_rpcrequest_async('RecognizeQrCode', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_qr_code(
        self,
        request: ocr_20191230_models.RecognizeQrCodeRequest,
    ) -> ocr_20191230_models.RecognizeQrCodeResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_qr_code_with_options(request, runtime)

    async def recognize_qr_code_async(
        self,
        request: ocr_20191230_models.RecognizeQrCodeRequest,
    ) -> ocr_20191230_models.RecognizeQrCodeResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_qr_code_with_options_async(request, runtime)

    def recognize_vincode_with_options(
        self,
        request: ocr_20191230_models.RecognizeVINCodeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeVINCodeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeVINCodeResponse().from_map(
            self.do_rpcrequest('RecognizeVINCode', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    async def recognize_vincode_with_options_async(
        self,
        request: ocr_20191230_models.RecognizeVINCodeRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeVINCodeResponse:
        UtilClient.validate_model(request)
        req = open_api_models.OpenApiRequest(
            body=UtilClient.to_map(request)
        )
        return ocr_20191230_models.RecognizeVINCodeResponse().from_map(
            await self.do_rpcrequest_async('RecognizeVINCode', '2019-12-30', 'HTTPS', 'POST', 'AK', 'json', req, runtime)
        )

    def recognize_vincode(
        self,
        request: ocr_20191230_models.RecognizeVINCodeRequest,
    ) -> ocr_20191230_models.RecognizeVINCodeResponse:
        runtime = util_models.RuntimeOptions()
        return self.recognize_vincode_with_options(request, runtime)

    async def recognize_vincode_async(
        self,
        request: ocr_20191230_models.RecognizeVINCodeRequest,
    ) -> ocr_20191230_models.RecognizeVINCodeResponse:
        runtime = util_models.RuntimeOptions()
        return await self.recognize_vincode_with_options_async(request, runtime)

    def recognize_vincode_advance(
        self,
        request: ocr_20191230_models.RecognizeVINCodeAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeVINCodeResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_vincode_req = ocr_20191230_models.RecognizeVINCodeRequest()
        OpenApiUtilClient.convert(request, recognize_vincode_req)
        auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        oss_client.post_object(upload_request, oss_runtime)
        recognize_vincode_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_vincode_resp = self.recognize_vincode_with_options(recognize_vincode_req, runtime)
        return recognize_vincode_resp

    async def recognize_vincode_advance_async(
        self,
        request: ocr_20191230_models.RecognizeVINCodeAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> ocr_20191230_models.RecognizeVINCodeResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            type='access_key',
            endpoint='openplatform.aliyuncs.com',
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='ocr',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        OpenApiUtilClient.convert(runtime, oss_runtime)
        recognize_vincode_req = ocr_20191230_models.RecognizeVINCodeRequest()
        OpenApiUtilClient.convert(request, recognize_vincode_req)
        auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
        oss_config.access_key_id = auth_response.access_key_id
        oss_config.endpoint = OpenApiUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
        oss_client = OSSClient(oss_config)
        file_obj = file_form_models.FileField(
            filename=auth_response.object_key,
            content=request.image_urlobject,
            content_type=''
        )
        oss_header = oss_models.PostObjectRequestHeader(
            access_key_id=auth_response.access_key_id,
            policy=auth_response.encoded_policy,
            signature=auth_response.signature,
            key=auth_response.object_key,
            file=file_obj,
            success_action_status='201'
        )
        upload_request = oss_models.PostObjectRequest(
            bucket_name=auth_response.bucket,
            header=oss_header
        )
        await oss_client.post_object_async(upload_request, oss_runtime)
        recognize_vincode_req.image_url = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        recognize_vincode_resp = await self.recognize_vincode_with_options_async(recognize_vincode_req, runtime)
        return recognize_vincode_resp
