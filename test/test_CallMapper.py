
    # This might need to run before the sanity check ? Or What would be the order between the terminologies?
    def test_calls_have_answers(self):
        # Might be an issue in the migrations file?
        # paths = [os.path.join(dp, f) for dp, dn, filenames in os.walk("../../../") for f in filenames if
        #           os.path.splitext(f)[1] == '.py']
        paths = ["../../../../hazardlog/base/models.py"]
        missing_keys = set()

        for file in paths:
            mapper = TestTerminologyCallsHaveAnswers._GetTermCallMapper()
            mapper.process(file)
            found = []
            for node, calls in mapper.calls.items():
                for method, arguments_list_collection in calls.items():
                    if method == "get_term": #TODO make regex to match exactly
                        for values in arguments_list_collection:
                                if DEFAULT_TERM.get(values[0]) is None:
                                    missing_keys.add(values[0])
        assert len(missing_keys) == 0
