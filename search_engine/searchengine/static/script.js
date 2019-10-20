let numResults;
let query = "";
const URL = "http://127.0.0.1:5000/";

const doSearch = function() {
	$(".results-wrapper").empty();

	query = $(".input-box").val();
	if (query.length == 0) {
		$(".no-result-wrapper").css("display", "flex");
		$(".no-result-prompt").html(
			`Your search "<p class="emphasis">${query}</p>" did not match any articles.`
		);
	} else {
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
						`Your search "<p class="emphasis">${query}</p>" did not match any articles.`
					);
				} else {
					for (var i = 0; i < num; i++) {
						let div = `
          <div class="single-result-wrapper">
            <div class="relevance-control-wrapper">
                <input value="${res.ids[i]}" class="relevance-radio" type="radio" id="rel_${i}" name="radio_${i}">
                <label class="radio-label radio-label-rel" for="rel_${i}">
                    <i class="relevance-button fa fa-caret-up"></i>
                </label>
                <input value="${res.ids[i]}" class="relevance-radio" type="radio" id="irrel_${i}" name="radio_${i}">
                <label class="radio-label radio-label-irrel" for="irrel_${i}">
                    <i class="relevance-button fa fa-caret-down"></i>
                </label>
            </div>
            <div class="result-contents-wrapper">
                <a id="${res.ids[i]}" class="result-title" href="${paperBaseUrl}${res.ids[i]}.pdf" target="_blank">${res.titles[i]}</a>
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
	}
};

// log link clicks
$(".results-wrapper").on("click", "a", function(e) {
	$.ajax({
		type: "POST",
		url: URL + "link-click",
		contentType: "application/json; charset=utf-8",
		data: JSON.stringify({ query: query, id: e.target.id })
	});
});

// log relevance selections
$(document).on("change", 'input[type="radio"]', e => {
	$.ajax({
		type: "POST",
		url: URL + "relevance-selection",
		contentType: "application/json; charset=utf-8",
		data: JSON.stringify({
			query: query,
			id: e.target.value,
			rel: e.target.id.split("_")[0] === "rel" ? 1 : 0
		})
	});
});

// search on enter press
$(".input-box").on("keyup", e => {
	if (e.keyCode === 13) {
		doSearch();
	}
});

// search on button press
$(".search-button").on("click", () => {
	doSearch();
});
