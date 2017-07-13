$(function () {

    function init() {
        // set active menu item
        $(".nav a").each(function () {
            var href = $(this).attr('href');
            if (new RegExp(href).test(window.location.toString())) {
                $(this).addClass('active');
            }
        });

        $("select[name=courses]").removeAttr("multiple");
        $("select[name=courses] option").each(function () {
            if ($(this).attr("selected")) {
                $(this).remove();
            }
        });
        hide_select_if_empty();
    }

    init();

    // hidden button and select for courses
    function hide_select_if_empty() {
        var select = $("select[name=courses]");
        if (select.find("option").length === 0) {
            select.addClass("invisible");
            $(".btn-add-course").addClass("invisible");
        }
    }

    function add_select(val, text) {
        var div = $("<div></div>");
        $("<div class='course' data-value='" + val + "'>" + text + "</div>").appendTo(div);
        var btn = $("<div class='btn-remove'><i class='fa fa-remove'></i></div>");

        btn.click(function () {
            var removed = $(this).parent();
            var sel = $("select[name=courses]");
            if (sel.hasClass("invisible")) {
                sel.removeClass("invisible");
                $(".btn-add-course").removeClass("invisible");
            }
            var course = removed.find(".course");
            var val = course.attr("data-value");
            var opt = document.createElement("option");
            $(opt).val(val).text(text).appendTo(sel);
            $("select[name=selected] option[value=" + val + "]").removeAttr("selected");
            removed.next("hr").remove();
            removed.remove();
        });

        btn.appendTo(div);
        div.appendTo("#selected");
        $("<hr class='clear'/>").appendTo("#selected");
    }

    $("select[name=selected] option").each(function () {
        if ($(this).attr("selected")) {
            add_select($(this).val(), $(this).text());
        }
    });


    $(".btn-add-course").click(function () {
        var select = $("select[name=courses]");
        var val = select.val();
        var text = select.find("option:selected").text();

        select.find("option:selected").appendTo("#id_selected_courses");
        $("select[name=selected] option[value=" + val + "]").attr("selected", "selected");

        select.find("option:selected").remove();

        hide_select_if_empty();
        add_select(val, text);
    });

    $("select.how-many").change(function () {
        var paginate_by = $(this).find(":selected").val();
        var url = window.location.toString();
        var re = /(paginate_by=)(\d+)/;
        if (re.test(url)) {
            url = url.replace(re, "$1" + paginate_by);
        } else {
            if (url.indexOf("?") < 0) {
                url += "?paginate_by=" + paginate_by;
            } else {
                url += "&paginate_by=" + paginate_by;
            }
        }
        window.location = url;
    });

    $("form").validate({
        rules: {
            name: "required",
            email: {
                required: true,
                email: true
            }
        },
        messages: {
            name: '<i class="fa fa-exclamation-triangle error-icon" aria-hidden="true"></i>This field is required',
            email: {
                required: '<i class="fa fa-exclamation-triangle error-icon" aria-hidden="true"></i>This field is required',
                email: '<i class="fa fa-exclamation-triangle error-icon" aria-hidden="true"></i>Please enter a valid email address!'
            },
            phone: '<i class="fa fa-exclamation-triangle error-icon" aria-hidden="true"></i>Please enter a valid phone number',
            mobile_phone: '<i class="fa fa-exclamation-triangle error-icon" aria-hidden="true"></i>Please enter a valid phone number',
        }
    });
});