import re

class MQApp(object):


    def __init__(self):
        super(MQApp,self).__init__()
        self._rule_task_map = {} 
        self._direct_task_map = {} 

    def route(self, _type, rule, **options):
        def decorator(f):
            self._add_task_rule(rule, f, _type, **options)
            return f
         
        return decorator

    def _add_task_rule(self, rule, task, _type="", **options):
        assert _type in ("", "direct", "rule")
        if _type in ("", "direct"):
            self._direct_task_map[rule] = task

        elif _type == "rule":
            self._rule_task_map[rule] = task

    def do(self, msg, topic, _type=""):
        task = None
        if _type in ("", "direct"):
            task = self._direct_task_map.get(topic, None)
            if task:
                return task(msg)
        elif _type == "rule":
            for task_rule, _task in self._rule_task_map.items():
                match = re.match(task_rule, topic)
                if match:
                    task = _task
                    break
        
            if task:
                if match:
                    task(msg, *match.groups())
                else:
                    task(msg)
        else:
            raise TypeError("rule type error")

        return None


