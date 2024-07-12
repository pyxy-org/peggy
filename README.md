# peggy
A simple PEG parser generator, focused on python's grammar. Mostly a wrapper for `pegen` as it exists in the cpython source.

It's different in that it directly uses `python.gram` from the cpython source. The problem with doing that is that all actions in that grammar are written for C code. For example:

```
# Class definitions
# -----------------

class_def[stmt_ty]:
    | a=decorators b=class_def_raw { _PyPegen_class_def_decorators(p, a, b) }
    | class_def_raw

class_def_raw[stmt_ty]:
    | invalid_class_def_raw
    | 'class' a=NAME t=[type_params] b=['(' z=[arguments] ')' { z }] ':' c=block {
        _PyAST_ClassDef(a->v.Name.id,
                     (b) ? ((expr_ty) b)->v.Call.args : NULL,
                     (b) ? ((expr_ty) b)->v.Call.keywords : NULL,
                     c, NULL, t, EXTRA) }
```

`peggy` makes this work by stripping all return types and actions from the grammar. Instead of actions, it returns the name of the rule it matched in addition to the matched tokens. This makes it useful if you just care about rules, which is all `pyxy` needs.

## Summary
### Disadvantages
* Can't differentiate between different cases of a rule that's matched
* Output data structure isn't the easiest to work with
### Advantages
* Uses the canonical Python grammar
* *Can* differentiate based on rule
