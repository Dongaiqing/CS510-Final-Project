const doSearch = () => {
    const searchQuery = $(".input-box").val();
    if (searchQuery.length !== 0) {
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/search",
            data: JSON.stringify({
                "query": searchQuery
            }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
        })
        .done((res) => {
            console.log(res.responseText);
        })
        .fail((err) => {
            console.log(err);
        })
        // $(".no-result-wrapper").css("display", "flex");
        // $(".no-result-prompt").html(`Your search "<p class="emphasis">${searchQuery}</p>" did not match any articles.`);
    }
}

$(".search-button").on("click", doSearch);
$(".input-box").on("keyup", (e) => {
    if (e.keyCode === 13)
        doSearch();
});