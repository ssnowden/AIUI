from browser import window, document, console, alert, bind


def main(*args, **kwargs):
    # console.log(f"with {args=} and {kwargs=}")

    SORT_HANDLE_ROW_CELL = 2
    ORDER_ROW_CELL = 5
    DELETE_ROW_CELL = 6
    INPUT_BOX = 0

    empty_list_item_form = document["empty-list-item-form"]
    form_container = document["formset-container"]
    total_forms = document["id_list_item-TOTAL_FORMS"]
    add_item_button = document["add-list-item-form"]

    def reorder_list_items(list_items_to_be_reordered):
        for index, form in enumerate(list_items_to_be_reordered):
            form.cells[ORDER_ROW_CELL].children[INPUT_BOX].value = index + 1

    def sortable_reorder_list_items(ev, ui):
        # Check for deleted and undeleted transition
        # console.log(f"trying to sort the items with {ev=} and {ui=}")
        for index, form in enumerate(document.querySelectorAll(".list-item-form")):
            form.cells[ORDER_ROW_CELL].children[INPUT_BOX].value = index + 1

    def move_list_item_form(form_to_be_moved, move_to, before=True):
        S(form_to_be_moved).remove()
        if before:
            S(form_to_be_moved).insertBefore(move_to)
        else:
            S(form_to_be_moved).insertAfter(move_to)
        reorder_list_items(document.querySelectorAll(".list-item-form"))

        add_item_button.disabled = False

    def enable_add_item_button(ev):
        if ev.target.value > "":
            add_item_button.disabled = False
        else:
            add_item_button.disabled = True

    def list_item_text_box_focus(ev):
        list_item_text_box_id = ev.target.id
        list_item_text_box = document[list_item_text_box_id]
        list_item_order = document.querySelectorAll(".list-item-form").length

        if list_item_text_box.value is "":
            list_item_order_box_id = list_item_text_box_id.replace("text", "ORDER")
            list_item_order_box = document[list_item_order_box_id]
            list_item_order_box.value = list_item_order

    def list_item_undelete(ev):
        target = S(ev.target)
        if target["is"]("button"):
            list_item_button = ev.target
            list_item_icon = ev.target.firstElementChild
            list_item_form = ev.target.parent.parent
        else:
            list_item_button = ev.target.parent
            list_item_icon = ev.target
            list_item_form = ev.target.parent.parent.parent

        list_item_form.attrs["class"] = "list-item-form"
        list_item_form.cells[SORT_HANDLE_ROW_CELL].style = {"cursor": "pointer"}
        check_box = S(list_item_form.cells[DELETE_ROW_CELL].children[INPUT_BOX])
        check_box.removeAttr("checked")
        list_item_button.attrs["class"] = "btn btn-danger mt-2 mt-xl-0"
        list_item_button.bind("click", list_item_mark_for_deletion)
        list_item_icon.attrs["class"] = "bi bi-trash"
        move_list_item_form(list_item_form, "#empty-list-item-form", before=True)

    def list_item_mark_for_deletion(ev):
        num_list_items = document.querySelectorAll(".list-item-form").length
        target = S(ev.target)
        if target["is"]("button"):
            list_item_button = ev.target
            list_item_icon = ev.target.firstElementChild
            list_item_form = ev.target.parent.parent
        else:
            list_item_button = ev.target.parent
            list_item_icon = ev.target
            list_item_form = ev.target.parent.parent.parent

        if num_list_items > 1:
            move_list_item_form(list_item_form, "#items-for-deletion", before=False)
            list_item_form.attrs["class"] = "list-item-form-marked-delete"
            list_item_form.cells[ORDER_ROW_CELL].children[INPUT_BOX].value = 0
            list_item_form.cells[SORT_HANDLE_ROW_CELL].style = {"cursor": "not-allowed"}
            check_box = S(list_item_form.cells[DELETE_ROW_CELL].children[INPUT_BOX])
            check_box.attr("checked", "checked")
            list_item_button.attrs["class"] = "btn btn-primary btn-rounded mt-2 mt-xl-0"
            list_item_button.bind("click", list_item_undelete)
            list_item_icon.attrs["class"] = "bi bi-plus-lg"

    @bind("#add-list-item-form", "click")
    def add_form(ev):
        ev.preventDefault()
        form_num = int(total_forms["value"])

        new_list_item_form = empty_list_item_form.cloneNode(True)
        new_list_item_form.innerHTML = new_list_item_form.innerHTML.replace(
            "__prefix__", f"{form_num}"
        )
        del new_list_item_form.attrs["hidden"]
        del new_list_item_form.attrs["id"]
        new_list_item_form.attrs["class"] = "list-item-form"

        S(new_list_item_form).insertBefore(S(empty_list_item_form))
        list_item_text_box = document[f"id_list_item-{form_num}-text"]
        list_item_text_box.bind("focus", list_item_text_box_focus)
        list_item_text_box.bind("input", enable_add_item_button)
        list_item_delete_button = document[f"id_list_item-{form_num}-mark-deleted"]
        list_item_delete_button.bind("click", list_item_mark_for_deletion)

        total_forms["value"] = form_num + 1
        add_item_button.disabled = True

    for index, _ in enumerate(document.querySelectorAll(".list-item-form")):
        list_item_text_box_initial = document[f"id_list_item-{index}-text"]
        list_item_text_box_initial.bind("focus", list_item_text_box_focus)
        list_item_text_box_initial.bind("input", enable_add_item_button)
        list_item_delete_button_initial = document[f"id_list_item-{index}-mark-deleted"]
        list_item_delete_button_initial.bind("click", list_item_mark_for_deletion)

    S("#formset-container").sortable(
        {
            "cursor": "move",
            "helper": "clone",
            "stop": sortable_reorder_list_items,
            "handle": "td.handle",
            "items": "> tr.list-item-form",
        }
    )


S = window.jQuery
S(document).ready(main)
