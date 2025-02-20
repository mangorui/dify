from flask import request
from flask_login import current_user, login_required
from flask_restful import Resource, inputs, marshal, reqparse
from werkzeug.exceptions import BadRequest, Forbidden

from controllers.console import api
from controllers.console.wraps import account_initialization_required, setup_required
from fields.app_fields import template_list_fields
from services.template_service import TemplateService


class TemplateListApi(Resource):
    def __init__(self):
        self.template_service = TemplateService()

    @setup_required
    @login_required
    @account_initialization_required
    def get(self):
        """Get template list"""
        parser = reqparse.RequestParser()
        parser.add_argument("page", type=inputs.int_range(1, 99999), required=False, default=1, location="args")
        parser.add_argument("limit", type=inputs.int_range(1, 100), required=False, default=20, location="args")
        args = parser.parse_args()

        # get template list
        auth_header = request.headers.get("Authorization")
        template_pagination = self.template_service.get_template_apps(current_user.current_tenant_id, args, auth_header)
        
        return marshal(template_pagination, template_list_fields)

    @setup_required
    @login_required
    @account_initialization_required
    def post(self):
        """Create template"""
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True, location="json")
        args = parser.parse_args()

        # The role of the current user in the ta table must be admin, owner, or editor
        if not current_user.is_editor:
            raise Forbidden()

        auth_header = request.headers.get("Authorization")
        result = self.template_service.create_template(current_user.current_tenant_id, args["name"], auth_header)
        
        if result["result"] == "error":
            raise BadRequest(result["message"])
            
        return result, 201


class TemplateApi(Resource):
    def __init__(self):
        self.template_service = TemplateService()

    @setup_required
    @login_required
    @account_initialization_required
    def get(self, template_id):
        """Get template detail"""
        auth_header = request.headers.get("Authorization")
        result = self.template_service.get_template_info(template_id, auth_header)
        
        if result["result"] == "error":
            raise BadRequest(result["message"])
            
        return result["data"]

    @setup_required
    @login_required
    @account_initialization_required
    def put(self, template_id):
        """Update template"""
        # The role of the current user in the ta table must be admin, owner, or editor
        if not current_user.is_editor:
            raise Forbidden()

        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=False, location="json")
        parser.add_argument("category", type=str, required=False, location="json")
        parser.add_argument("content", type=str, required=False, location="json")
        parser.add_argument("status", type=int, required=False, location="json")
        args = parser.parse_args()

        # 构建更新数据
        template_data = {
            "id": template_id,
            "name": args["name"],
            "category": args.get("category", ""),
            "content": args.get("content", ""),
            "status": args.get("status", 0)
        }

        auth_header = request.headers.get("Authorization")
        result = self.template_service.update_template(template_data, auth_header)
        
        if result["result"] == "error":
            raise BadRequest(result["message"])
            
        return result, 200

    @setup_required
    @login_required
    @account_initialization_required
    def delete(self, template_id):
        """Delete template (set status to 1)"""
        # The role of the current user in the ta table must be admin, owner, or editor
        if not current_user.is_editor:
            raise Forbidden()

        # 构建删除数据 (通过设置 status=1 来标记删除)
        template_data = {
            "id": template_id,
            "status": 1  # 使用状态1表示删除
        }

        auth_header = request.headers.get("Authorization")
        result = self.template_service.update_template(template_data, auth_header)
        
        if result["result"] == "error":
            raise BadRequest(result["message"])
            
        return {"result": "success"}, 204  # 使用204状态码表示成功删除


# 注册 API 路由
api.add_resource(TemplateListApi, '/templates')
api.add_resource(TemplateApi, '/templates/<int:template_id>') 