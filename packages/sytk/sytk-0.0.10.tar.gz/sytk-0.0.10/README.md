# sytk
Some tools making life a little easier :)
## @admin
Apply for the administrator right for the decorated function.
## @cache
Cache the `{'func-params': return value}` of the decorated functions. It is mainly used on functions calculating duplicate data.
## @debug
+ Show `parameters` and `return value` of the decorated function in a vivid color.
+ Meanwhile, in the same usage with `print()`, `d_print()`is also available to show the debug information in functions decorated with `@debug`.
## @print2log
+ Redirect all the context printed by `print()` into file named `{file}_[{func}].log`.
+ It can also catch Exception.
## clean(path)
Delete code lines containing '@debug' and 'd_print'. It is used to turn projects into productions.
