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

var numResults;
var query ="";
var URL = "http://127.0.0.1:5000/";
var id = "";


var doSearch = function() {
  $(".results-wrapper").empty();

  $.ajax({
    type: 'POST',
    url: URL+"search",
    data: JSON.stringify({query: query}),

    contentType: "applicaton/json; charset=utf-8",
    success: function(res)
    {
      var num = Math.min(res.titles.length, 10);
      //TODO: # documents less than 10
      if(num == 0) {
        $(".no-result-wrapper").css("display", "flex");
        $(".no-result-prompt").html(`Your search "<p class="emphasis">${searchQuery}</p>" did not match any articles.`);
      } else{
        for (var i = 0; i < num; i++) {
          $(".results-wrapper").append("<div class="single-result-wrapper">");
          buttons = "<div class="relevance-control-wrapper"><input class="relevance-radio" type="radio" id="rel" name="radio"><label class="radio-label radio-label-rel" for="rel"><i class="relevance-button fa fa-caret-up"></i></label><input class="relevance-radio" type="radio" id="irrel" name="radio"><label class="radio-label radio-label-irrel" for="irrel"><i class="relevance-button fa fa-caret-down"></i></label></div>";
          $(".results-wrapper").append(buttons);
          $(".results-wrapper").append("<div class="result-contents-wrapper"><a class="result-title" href="asd">")
          $(".results-wrapper").append(res.titles[i]);
          $(".results-wrapper").append("</a><p class="result-abstract">");
          $(".results-wrapper").append(res.abstracts[i]);
          $(".results-wrapper").append("</p></div> </div>");
        }
        $(".results-wrapper").append("</div>");
      }

    }
  });
};

$(document).ready(function(){
    $(".search-button").click(function(){
      query = $(".input-box").val();
      doSearch();
    });
    //relevance
    $(".results-wrapper").on("change", function(){
      var val = $(this).val();
      $.ajax({
       type: 'POST',
       url: URL + "relevance-selection",
       data: JSON.stringify({query: query, id: id, rel: val}),
      });
    });

    //link_click_log
    $(".results-wrapper").delegate("a", "click", function(){
      var url = this.id;
      $.ajax({
        type:'POST',
        url: URL + "link-click",
        data: JSON.stringify({query: query, id: url}),
      });
    });
    $(".input-box").on("keyup", (e) => {
        if (e.keyCode === 13) {
          $(".search-button");
        }
    });



});
