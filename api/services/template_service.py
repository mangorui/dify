import logging

import requests

from configs import dify_config


class TemplateService:
    def get_template_apps(self, tenant_id: str, args: dict, auth_header: str) -> dict:
        """
        Get template apps from external API
        :param args: request args containing page and limit
        :param auth_header: Authorization header to be passed to the API
        :return: dict with pagination info and template list
        """
        yaovia_url = dify_config.YAOVIA_API_URL
        logging.info(f"YAOVIA_API_URL from config: {yaovia_url}")
        
        if not yaovia_url:
            logging.error("YAOVIA_API_URL not found in configuration")
            return {
                "items": [],
                "total": 0,
                "page": args["page"],
                "per_page": args["limit"],
                "has_next": False
            }
        
        try:
            api_url = f"{yaovia_url}/amp/reporttemplate/list"
            logging.info(f"Requesting template from: {api_url}")
            
            # 添加 Authorization header
            headers = {'Authorization': auth_header} if auth_header else {}
            
            response = requests.get(
                api_url,
                params={
                    "page": args["page"],
                    "limit": args["limit"],
                    "tenant_id": tenant_id
                },
                headers=headers
            )
            response.raise_for_status()
            template_data = response.json()
            
            logging.info(f"Get template response: {template_data}")
            # 检查响应码
            if template_data.get("code") != 200:
                return {
                    "items": [],
                    "total": 0,
                    "page": args["page"],
                    "per_page": args["limit"],
                    "has_next": False
                }
            
            return {
                "items": template_data["data"]["list"],
                "total": template_data["data"]["total"],
                "page": args["page"],
                "per_page": args["limit"],
                "has_next": template_data["data"]["total"] > (args["page"] * args["limit"])
            }
            
        except requests.RequestException as e:
            logging.error(f"Failed to fetch templates: {str(e)}")
            return {
                "items": [],
                "total": 0,
                "page": args["page"],
                "per_page": args["limit"],
                "has_next": False
            }

    def create_template(self, tenant_id: str, name: str, auth_header: str) -> dict:
        """
        Create template via external API
        :param name: template name
        :param auth_header: Authorization header to be passed to the API
        :return: dict with response info
        """
        yaovia_url = dify_config.YAOVIA_API_URL
        logging.info(f"YAOVIA_API_URL from config: {yaovia_url}")
        
        if not yaovia_url:
            logging.error("YAOVIA_API_URL not found in configuration")
            return {"result": "error", "message": "YAOVIA_API_URL not configured"}
        
        try:
            api_url = f"{yaovia_url}/amp/reporttemplate/create"
            logging.info(f"Creating template at: {api_url}")
            
            # 添加 Authorization header
            headers = {
                'Authorization': auth_header,
                'Content-Type': 'application/json'
            } if auth_header else {}
            
            response = requests.post(
                api_url,
                json={"name": name, "tenant_id": tenant_id},
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            
            logging.info(f"Create template response: {result}")
            
            if result.get("code") != 200:
                return {"result": "error", "message": result.get("msg", "Unknown error")}
            
            return {"result": "success"}
            
        except requests.RequestException as e:
            logging.error(f"Failed to create template: {str(e)}")
            return {"result": "error", "message": str(e)}

    def get_template_info(self, template_id: int, auth_header: str) -> dict:
        """
        Get template detail information
        :param template_id: template id
        :param auth_header: Authorization header to be passed to the API
        :return: dict with template info
        """
        yaovia_url = dify_config.YAOVIA_API_URL
        logging.info(f"YAOVIA_API_URL from config: {yaovia_url}")
        
        if not yaovia_url:
            logging.error("YAOVIA_API_URL not found in configuration")
            return {"result": "error", "message": "YAOVIA_API_URL not configured"}
        
        try:
            api_url = f"{yaovia_url}/amp/reporttemplate/info"
            logging.info(f"Getting template info from: {api_url}")
            
            # 添加 Authorization header
            headers = {'Authorization': auth_header} if auth_header else {}
            
            response = requests.get(
                api_url,
                params={"id": template_id},
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            
            logging.info(f"Get template info response: {result}")
            
            if result.get("code") != 200:
                return {"result": "error", "message": result.get("msg", "Unknown error")}
            
            return {"result": "success", "data": result["data"]}
            
        except requests.RequestException as e:
            logging.error(f"Failed to get template info: {str(e)}")
            return {"result": "error", "message": str(e)}

    def update_template(self, template_data: dict, auth_header: str) -> dict:
        """
        Update template via external API
        :param template_data: template data including id, name, category, content and status
        :param auth_header: Authorization header to be passed to the API
        :return: dict with response info
        """
        yaovia_url = dify_config.YAOVIA_API_URL
        logging.info(f"YAOVIA_API_URL from config: {yaovia_url}")
        
        if not yaovia_url:
            logging.error("YAOVIA_API_URL not found in configuration")
            return {"result": "error", "message": "YAOVIA_API_URL not configured"}
        
        try:
            api_url = f"{yaovia_url}/amp/reporttemplate/update"
            logging.info(f"Updating template at: {api_url}")
            
            # 添加 Authorization header
            headers = {
                'Authorization': auth_header,
                'Content-Type': 'application/json'
            } if auth_header else {}
            
            response = requests.post(
                api_url,
                json=template_data,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            
            if template_data["status"] != 0:
                logging.info(f"Template {template_data['id']} has been marked as deleted.")
            else:
                logging.info(f"Template {template_data['id']} has been updated.")
            
            if result.get("code") != 200:
                return {"result": "error", "message": result.get("msg", "Unknown error")}
            
            return {"result": "success"}
            
        except requests.RequestException as e:
            logging.error(f"Failed to update template: {str(e)}")
            return {"result": "error", "message": str(e)} 