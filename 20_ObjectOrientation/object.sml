fun newObj(n) =
    let
      val c = ref n
    in
      {
        inc = fn() => c := 1 + !c,
        get = fn() => !c
      }
    end

val c0 = newObj(4);
val c1 = newObj(2);
#get c0();
#get c1();
#inc c0();
#get c0();
#get c1();
