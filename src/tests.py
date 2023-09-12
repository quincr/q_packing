import packing

successful_tests = 0
total_tests = 0

def do_test(write_func, read_func, value, test_name : str, should_err : bool):
    global successful_tests, total_tests
    total_tests += 1

    try:    
        _written = write_func(value)

        _read = read_func(_written)[1]

        if value == _read:
            if should_err:
                print("[ERR]", test_name)
                return
            print("[OK]", test_name)
            successful_tests += 1
        else:
            print("[ERR]", test_name)
    except:
        if should_err:
            print("[OK]", test_name)
            successful_tests += 1
            return
        print("[ERR]", test_name)
        return

do_test(packing.VarInt.Write, packing.VarInt.Read, 8971234, "Variable-length Integer Positive", False)
do_test(packing.VarInt.Write, packing.VarInt.Read, -217483, "Variable-length Integer Negative", False)
do_test(packing.VarInt.Write, packing.VarInt.Read, 3000000000, "Variable-length Integer Overflow", True)
do_test(packing.VarInt.Write, packing.VarInt.Read, -3000000000, "Variable-length Integer Underflow", True)

do_test(packing.Int.Write, packing.Int.Read, 8971234, "Integer Positive", False)
do_test(packing.Int.Write, packing.Int.Read, -217483, "Integer Negative", False)
do_test(packing.Int.Write, packing.Int.Read, 3000000000, "Integer Overflow", True)
do_test(packing.Int.Write, packing.Int.Read, -3000000000, "Integer Underflow", True)

do_test(packing.UInt.Write, packing.UInt.Read, -4000000000, "Unsigned Integer Negative", True)
do_test(packing.UInt.Write, packing.UInt.Read, 4000000000, "Unsigned Integer Positive", False)
do_test(packing.UInt.Write, packing.UInt.Read, 5000000000, "Unsigned Integer Overflow", True)
do_test(packing.UInt.Write, packing.UInt.Read, -8254, "Unsigned Integer Underflow", True)

print(f"Failed {total_tests - successful_tests} tests.")