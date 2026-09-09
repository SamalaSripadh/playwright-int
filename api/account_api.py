from api.base_client import BaseClient


class AccountApi(BaseClient):
    def create_account(self, account):
        response = self.request("POST", "/createAccount", data=account)
        if response.json().get("responseCode") == 400:
            response = self.request("POST", "/createAccount", data=account)
        return response

    def verify_login(self, email, password):
        return self.request(
            "POST",
            "/verifyLogin",
            data={"email": email, "password": password},
        )

    def update_account(self, account):
        return self.request("PUT", "/updateAccount", data=account)

    def get_user_detail(self, email):
        return self.request("GET", "/getUserDetailByEmail", params={"email": email})

    def delete_account(self, email, password):
        return self.request(
            "DELETE",
            "/deleteAccount",
            data={"email": email, "password": password},
        )