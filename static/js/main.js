
// Product Review Save
$("#addForm").submit(function(e){
	$.ajax({
		data:$(this).serialize(),
		method:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType:'json',
		success:function(res){
			if(res.bool==true){
				$(".ajaxRes").html('Data has been added.');
				$("#reset").trigger('click');
				// Hide Button
				$(".reviewBtn").hide();
				// End

				// create data for review
				var _html='<blockquote class="blockquote text-right">';
				_html+='<small>'+res.data.review_text+'</small>';
				_html+='<footer class="blockquote-footer">'+res.data.user;
				_html+='<cite title="Source Title">';
				for(var i=1; i<=res.data.review_rating; i++){
					_html+='<i class="fa fa-star text-warning"></i>';
				}
				_html+='</cite>';
				_html+='</footer>';
				_html+='</blockquote>';
				_html+='</hr>';

				$(".no-data").hide();

				// Prepend Data
				$(".review-list").prepend(_html);

				// Hide Modal
				$("#productReview").modal('hide');

				// AVg Rating
				$(".avg-rating").text(res.avg_reviews.avg_rating.toFixed(1))
			}
		}
	});
	e.preventDefault();
});
// End
