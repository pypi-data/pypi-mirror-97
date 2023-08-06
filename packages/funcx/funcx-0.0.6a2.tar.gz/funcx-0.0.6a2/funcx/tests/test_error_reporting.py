from funcx.sdk.client import FuncXClient
import pytest
import time


def div_0():
    return 1 / 0


def numpy_error():
    import numpy as np
    np.seterr(all='raise')
    return np.array([1]) / 0


def missing_import():
    import NonExistent
    return


test_cases = [(div_0, ZeroDivisionError),
              (numpy_error, FloatingPointError),
              (missing_import, ImportError),
]


@pytest.mark.parametrize('fn,exception', test_cases)
def test_params(fxc, endpoint, fn, exception):

    try:
        fn()
    except exception:
        return
    else:
        raise Exception("Wrong exception raised")

    """
    fn_uuid = fxc.register_function(fn, endpoint, description='arb_fn')

    task_id = fxc.run(param,
                      endpoint_id=endpoint,
                      function_id=fn_uuid)

    flag = False
    for i in range(5):
        try:
            r = fxc.get_result(task_id)
            print(f"result : {r}")
        except Exception:
            time.sleep(2)
        else:
            flag = True
            break

    assert flag, "Task failed to return in 5s"
    """
