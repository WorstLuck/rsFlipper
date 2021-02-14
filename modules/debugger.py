from textwrap import dedent
import os

def show_callbacks(app):

    def wrap_list(items, padding=24):
        return ("\n"+" "*padding).join(items)

    def format_regs(registrations):
        vals = sorted("{}.{}".format(i['id'], i['property'])
                      for i in registrations)
        return wrap_list(vals)

    output_list = []

    for callback_id, callback in app.callback_map.items():
        wrapped_func = callback["callback"].__wrapped__
        inputs = callback["inputs"]
        states = callback["state"]

        if callback_id.startswith(".."):
            outputs = callback_id.strip(".").split("...")
        else:
            outputs = [callback_id]

        str_values = {
            "callback": wrapped_func.__name__,
            "outputs": wrap_list(outputs),
            "filename": os.path.split(wrapped_func.__code__.co_filename)[-1],
            "lineno": wrapped_func.__code__.co_firstlineno,
            "num_inputs": len(inputs),
            "num_states": len(states),
            "inputs": format_regs(inputs),
            "states": format_regs(states),
            "num_outputs": len(outputs),
        }

        output = dedent(
            """                                                                                                                                                                                                      
            callback    {callback} @ {filename}:{lineno}                                                                                                                                                             
            Outputs{num_outputs:>3}  {outputs}                                                                                                                                                                       
            Inputs{num_inputs:>4}  {inputs}                                                                                                                                                                          
            States{num_states:>4}  {states}                                                                                                                                                                          
            """.format(**str_values)
        )

        output_list.append(output)
    return "\n".join(output_list)