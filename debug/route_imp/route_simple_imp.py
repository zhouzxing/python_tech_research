class RouterMeta(type):
    """元类：自动收集被 @route 标记的方法"""
    def __new__(mcs, name, bases, namespace):
        routes = {}
        for key, value in namespace.items():
            if hasattr(value, "_route_path"):
                routes[value._route_path] = (value._http_method, key)
        namespace["_routes"] = routes
        return super().__new__(mcs, name, bases, namespace)


def route(path, method="GET"):
    """装饰器：给方法打上路由标记"""
    def decorator(func):
        func._route_path = path
        func._http_method = method
        return func
    return decorator


class Controller(metaclass=RouterMeta):
    """所有控制器的基类"""

    @classmethod
    def dispatch(cls, path, method):
        if path not in cls._routes:
            return 404, "Not Found"
        http_method, func_name = cls._routes[path]
        if http_method != method:
            return 405, "Method Not Allowed"
        return 200, getattr(cls(), func_name)()


# ===== 使用 =====
class UserController(Controller):
    @route("/users", "GET")
    def list_users(self):
        return [{"id": 1, "name": "Alice"}]

    @route("/users/create", "POST")
    def create_user(self):
        return {"status": "created"}


print(UserController._routes)
# {'/users': ('GET', 'list_users'), '/users/create': ('POST', 'create_user')}

print(UserController.dispatch("/users", "GET"))
# (200, [{'id': 1, 'name': 'Alice'}])

print(UserController.dispatch("/users", "POST"))
# (405, 'Method Not Allowed')

print(UserController.dispatch("/unknown", "GET"))
# (404, 'Not Found')