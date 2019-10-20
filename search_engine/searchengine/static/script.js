const doSearch = () => {
    const searchQuery = $(".input-box").val();
    if (searchQuery.length !== 0) {
        $(".no-result-wrapper").css("display", "flex");
        $(".no-result-prompt").html(`Your search "<p class="emphasis">${searchQuery}</p>" did not match any articles.`);
    }
}

$(".search-button").on("click", doSearch);
$(".input-box").on("keyup", (e) => {
    if (e.keyCode === 13)
        doSearch();
});