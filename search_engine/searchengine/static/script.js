let numResults;
let query = "";
const URL = "http://127.0.0.1:5000/";

const doSearch = function() {
	$(".results-wrapper").empty();
	const uid = localStorage.getItem("uid");
	query = $(".input-box").val();
	if (query.length !== 0) {
		$.ajax({
			type: "POST",
			url: URL + "search",
			data: JSON.stringify({
				query: query,
				uid: uid === null ? "" : uid
			}),
			contentType: "application/json; charset=utf-8",
			success: function(res) {
				var num = Math.min(res.titles.length, 10);
				//TODO: # documents less than 10
				if (num === 0) {
					$(".no-result-wrapper").css("display", "flex");
					$(".no-result-prompt").html(
						`Your search "<p class="emphasis">${query}</p>" did not match any articles.`
					);
				} else {
					for (var i = 0; i < num; i++) {
						let div = 
		`<div class="single-result-wrapper">
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
                <a id="${res.ids[i]}" class="result-title">${res.titles[i]}</a>
                <p class="result-abstract">${res.abstracts[i]}</p>
            </div>
        </div>`;
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
	// track time user spent on paper
	localStorage.setItem("starttime", new Date().getTime());

	const pid = e.target.id;
	const uid = localStorage.getItem("uid");
	const paperBaseUrl = "https://www.aclweb.org/anthology/";
	const pdfUrl = `${paperBaseUrl}${pid}.pdf`;
	let pdfPreviewDiv = `
		<div class="pdf-overlay">
			<i class="pdf-close-bt fas fa-times-circle"></i>
			<object data="${pdfUrl}" style="width:100%; height:100%;"></object>
		</div>`;
	$("body").append(pdfPreviewDiv);
	$(".pdf-close-bt").on("click", () => {
		$(".pdf-overlay").css("display", "none");
		$(".pdf-overlay").remove();

		const start = localStorage.getItem("starttime");
		const end = new Date().getTime();
		localStorage.removeItem("starttime");

		$.ajax({
			type: "POST",
			url: URL + "link-click",
			contentType: "application/json; charset=utf-8",
			data: JSON.stringify({
				query: query,
				pid: pid,
				uid: uid === null ? "" : uid,
				time: (end - start) / 1000
			})
		});
	});
});

// log relevance selections
$(document).on("change", 'input[type="radio"]', e => {
	const uid = localStorage.getItem("uid");
	$.ajax({
		type: "POST",
		url: URL + "relevance-selection",
		contentType: "application/json; charset=utf-8",
		data: JSON.stringify({
			query: query,
			pid: e.target.value,
			rel: e.target.id.split("_")[0] === "rel" ? 1 : 0,
			uid: uid === null ? "" : uid
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

$("#uid-submission-bt").on("click", () => {
	setUid();
});

$("#uid-input").on("keyup", e => {
	if (e.keyCode === 13) {
		setUid();
	}
});

$("#log-out-button").on("click", () => {
	localStorage.removeItem("uid");
	$("#uid-input").val("");
	displayUid();
});

const displayUid = () => {
	let uid = localStorage.getItem("uid");
	console.log("UID: " + uid);
	if (uid !== null) {
		$("#uid-input-wrapper").css("display", "none");
		$("#log-out-wrapper").css("display", "flex");
		$(".uid-p").text(uid);
	} else {
		$("#log-out-wrapper").css("display", "none");
		$("#uid-input-wrapper").css("display", "flex");
	}
};

const setUid = () => {
	let uidInput = $("#uid-input").val();
	if (uidInput !== "") {
		localStorage.setItem("uid", uidInput);
		displayUid();

		$.ajax({
			type: "POST",
			url: URL + "login",
			contentType: "application/json; charset=utf-8",
			data: JSON.stringify({ uid: uidInput })
		});
	}
};

$(document).ready(() => {
	displayUid();
});
