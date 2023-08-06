class EventTestCase:
    def __init__(self, call_watch_event_fn=None, effective_print: str = "", in_result_fn=None):
        self.event_fn = call_watch_event_fn
        self.label_effective = effective_print
        self.in_result = in_result_fn

    def Exec(self):
        result = self.event_fn
        if len(result) > 0:
            print(self.label_effective)
            if "transaction_id" in result[0] and "result" in result[0]:
                if self.in_result is not None:
                    self.in_result(result[0]["result"])
