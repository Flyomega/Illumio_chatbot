import gradio as gr
from src.control.control import Controller


def run(ctrl: Controller, config: {}):
    with gr.Blocks() as qna:
        with gr.Row():
            with gr.Column():
                pass

            with gr.Column(scale=10):

                gr.Markdown(config['title'])

                histo_text_comp = gr.Chatbot(
                    visible=False,
                    value=[],
                )
                input_text_comp = gr.Textbox(
                    label="",
                    lines=1,
                    max_lines=3,
                    interactive=True,
                    placeholder="Posez votre question ici",
                )
                clear_btn = gr.Button("Clear")
                input_example_comp = gr.Radio(
                    label="Examples",
                    choices=list(config['examples'].values()),
                    value="",
                )
                source_text_comp = []
                for i in range(4):
                    source_text_comp.append(gr.Textbox(
                        lines=4,
                        max_lines=4,
                        interactive=False,
                        visible=False,
                    ))

            with gr.Column():
                pass

        def input_text_fn1(input_text_, histo_text_):
            histo_text_.append((input_text_, None))
            update_ = {
                histo_text_comp: gr.update(visible=True, value=histo_text_),
                input_example_comp: gr.update(visible=False,),
            }
            for i in range(4):
                update_[source_text_comp[i]] = gr.update(visible=False)
            return update_

        def input_text_fn2(input_text_, histo_text_):
            answer, sources = ctrl.get_response(query_fr=input_text_, histo_fr=histo_text_)
            histo_text_[-1] = (input_text_, answer)
            update_ = {
                histo_text_comp: gr.update(value=histo_text_),
                input_text_comp: gr.update(value=''),
            }
            for i in range(min(len(sources), 3)):
                s = sources[i]
                source_label = f'{s.index}   {s.title_fr}                        score = {s.distance_str}'
                source_text = s.content_fr
                update_[source_text_comp[i]] = gr.update(visible=True, value=source_text, label=source_label)
            return update_

        def input_example_fn(input_example_, histo_text_):
            histo_text_.append((input_example_, None))
            update_ = {
                input_text_comp: gr.update(value=input_example_),
                histo_text_comp: gr.update(visible=True, value=histo_text_),
                input_example_comp: gr.update(visible=False, value=''),
            }
            for i in range(4):
                update_[source_text_comp[i]] = gr.update(visible=False)
            return update_

        def clear_fn():
            update_ = {
                input_text_comp: gr.update(value=''),
                histo_text_comp: gr.update(value='', visible=False),
                input_example_comp: gr.update(value='', visible=True),
            }
            for i in range(4):
                update_[source_text_comp[i]] = gr.update(visible=False, value='hello')
            return update_

        input_text_comp \
            .submit(input_text_fn1,
                    inputs=[input_text_comp, histo_text_comp],
                    outputs=[histo_text_comp, input_example_comp,
                             source_text_comp[0], source_text_comp[1], source_text_comp[2], source_text_comp[3]])\
            .then(input_text_fn2,
                  inputs=[input_text_comp, histo_text_comp],
                  outputs=[input_text_comp, histo_text_comp,
                           source_text_comp[0], source_text_comp[1], source_text_comp[2], source_text_comp[3]])
        input_example_comp \
            .input(input_example_fn,
                   inputs=[input_example_comp, histo_text_comp],
                   outputs=[input_text_comp, histo_text_comp, input_example_comp,
                            source_text_comp[0], source_text_comp[1], source_text_comp[2], source_text_comp[3]])\
            .then(input_text_fn2,
                  inputs=[input_text_comp, histo_text_comp],
                  outputs=[input_text_comp, histo_text_comp,
                           source_text_comp[0], source_text_comp[1], source_text_comp[2], source_text_comp[3]])
        clear_btn.click(clear_fn,
                        inputs=None,
                        outputs=[input_text_comp, histo_text_comp, input_example_comp,
                                 source_text_comp[0], source_text_comp[1], source_text_comp[2], source_text_comp[3]])

    return qna
