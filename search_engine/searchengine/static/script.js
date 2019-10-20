let numResults;
let query = "";
const URL = "http://127.0.0.1:5000/";

const doSearch = function() {
	$(".results-wrapper").empty();

	$.ajax({
		type: "POST",
		url: URL + "search",
		data: JSON.stringify({ query: query }),

		contentType: "application/json; charset=utf-8",
		success: function(res) {
            const paperBaseUrl = "https://www.aclweb.org/anthology/";
			var num = Math.min(res.titles.length, 10);
			//TODO: # documents less than 10
			if (num == 0) {
				$(".no-result-wrapper").css("display", "flex");
				$(".no-result-prompt").html(
					`Your search "<p class="emphasis">${searchQuery}</p>" did not match any articles.`
				);
			} else {
				for (var i = 0; i < num; i++) {

					let div = `
          <div id="${res.ids[i]}" class="single-result-wrapper">
            <div class="relevance-control-wrapper">
                <input value="${res.ids[i]}" class="relevance-radio" type="radio" id="rel" name="radio">
                <label class="radio-label radio-label-rel" for="rel">
                    <i class="relevance-button fa fa-caret-up"></i>
                </label>
                <input value="${res.ids[i]}" class="relevance-radio" type="radio" id="irrel" name="radio">
                <label class="radio-label radio-label-irrel" for="irrel">
                    <i class="relevance-button fa fa-caret-down"></i>
                </label>
            </div>
            <div class="result-contents-wrapper">
                <a class="result-title" href="${paperBaseUrl}${res.ids[i]}.pdf">${res.titles[i]}</a>
                <p class="result-abstract">${res.abstracts[i]}</p>
            </div>
        </div>
          `;
					$(".results-wrapper").append(div);
				}
				$(".results-wrapper").append("</div>");
			}
		}
	});
};

$(".search-button").click(function() {
    query = $(".input-box").val();
    if (query.length == 0) {
        $(".no-result-wrapper").css("display", "flex");
        $(".no-result-prompt").html(
            'Your search "<p class="emphasis">${query}</p>" did not match any articles.'
        );
    }
    doSearch();
});

//link_click_log
$(".results-wrapper").delegate("a", "click", function() {
    var url = this.id;
    $.ajax({
        type: "POST",
        url: URL + "link-click",
        data: JSON.stringify({ query: query, id: url })
    });
});
$(".input-box").on("keyup", e => {
    if (e.keyCode === 13) {
        doSearch();
    }
});
$('input[name="pid_1"]:radio').change(() => {
    console.log(2);
    if (this.checked) {
        $.ajax({
            type: "POST",
            url: URL + "relevance-selection",
            data: JSON.stringify({ query: query, id: this.value, rel: this.id === "rel" ? 1 : 0 })
        });
    }
});

