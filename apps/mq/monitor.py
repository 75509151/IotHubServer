from collections import defaultdict
import re

class MQApp(object):


    def __init__(self):
        super(MQApp,self).__init__()
        self._rule_task_map = defaultdict()
        self._direct_task_map = defaultdict()

    def route(self, _type, rule, **options):
        def decorator(f):
            self.add_task_rule(_type, rule, f, **options)
            return f
         
        return decorator

    def add_task_rule(self, task, rule, _type, **options):
        assert _type in ("", "direct", "route")
        if _type in ("", "direct"):
            self._direct_task_map[rule] = task

        elif _type == "rule":
            self._rule_task_map.setdefault(_type, {})
            self._rule_task_map[_type][rule] = task

    def do(self, msg, rule, _type=""):
        task = None
        if _type in ("", "direct"):
            task = self._direct_task_map.get(rule, None)
            if task:
                return task(msg)
        elif _type == "rule":
            match = None
            for task_rule, _task in self._rule_task_map.items():
                match = re.match(task_rule, rule)
                if match:
                    task = _task
                    break
            if task:
                if match:
                    return task(msg, *match.groups())
                else:
                    return task(msg)
        
        else:
            raise TypeError("rule type error")

        return None


