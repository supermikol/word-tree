$(document).ready(function() {
  $('.rating-checkbox').on('change', function() {
    var aHrefVals = [];

    $('.rating-checkbox').filter(":checked").each(function() {
        aHrefVals.push($(this).val());
    });

    $(".product-link").attr("href", function(i, val) {
      let with_rating = val.split('rating')[0]+ 'rating=' + aHrefVals.join(",")
      // console.log(with_rating)
      return with_rating
    }); 
  })
})