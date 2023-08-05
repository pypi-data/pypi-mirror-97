from re import findall


class Activity:
    __endpoints = {
        'activities': ('get', '/activities'),
        'activity': ('get', '/activities/{activityId}'),
        'cancel': ('post', '/activities/{activityId}/cancel'),
        'delete': ('delete', '/activities/{activityId}'),
        'hold': ('post', '/activities/{activityId}/hold'),
        'release': ('post', '/activities/{activityId}/release'),
        'retry': ('post', '/activities/{activityId}/retry'),
        'steps': ('get', '/activities/{activityId}/steps'),
        'step': ('get', '/activities/{activityId}/steps/{stepId}'),
        'step_logs': ('get', '/activities/{activityId}/steps/{stepId}/logs'),
        'continue': ('post', '/activities/{activityId}/steps/{stepId}/continue'),
        'create_activity': ('post', '/activities'),
    }

    def __init__(self, parent):
        self.__parent = parent
        self._build_url = parent._build_url
        self.connection = parent._connection

    def get_all(self):
        endpoint = self.__endpoints.get('activities')

        return self.connection.request(
            self._build_url(endpoint[1]),
            endpoint[0],
        )

    def get(self, activity_id):
        endpoint = self.__endpoints.get('activity')
        params = {'activityId': activity_id}

        return self.connection.request(
            self._build_url(endpoint[1], params),
            endpoint[0],
        )

    def execute_job_template(self, template_name, *, dry_run=False):
        endpoint = self.__endpoints.get('create_activity')
        data = {'type': 'operationTemplate',
                'operation': template_name,
                'validateOnly': dry_run}

        return self.connection.request(
            self._build_url(endpoint[1]),
            endpoint[0],
            data=data
        )

    def activity_status(self, *, days=1, fields='items(description,status,beginTime)', user=None, dry_run=False):
        endpoint = self.__endpoints.get('activities')
        params = {
            'user': user,
            'days': days,
            'fields': fields
        }

        return self.connection.request(
            self._build_url(endpoint[1]),
            endpoint[0],
            params=params
        )

    def naive_request(self, endpoint, *, params={}, data={}, headers={}):
        if endpoint not in self.__endpoints.keys():
            raise ValueError(
                f'endpoint must be one of {self.__endpoints.keys()}')

        endpoint = self.__endpoints.get(endpoint)

        required_params = findall(r'\{(.*?)\}', endpoint[1])
        for param in required_params:
            if param not in params.keys():
                raise ValueError(
                    f'missing parameter "{param}"')

        return self.connection.request(
            self._build_url(endpoint[1], params),
            endpoint[0],
            data=data,
            headers=headers
        )
