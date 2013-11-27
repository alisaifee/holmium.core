$(function () {
    $(".reference-link").click(function (event) {
        event.preventDefault();
        link = $(this).attr("href");
        $.ajax(
            {
                url: "/reference/" + link,
                context: document.body
            }
        ).done(
            function (data) {
                $("#reference-content").html(data.data);
            }
        )
    });
});
