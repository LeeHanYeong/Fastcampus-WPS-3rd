function photoLike(photoPk, likeType) {
    var url = '/photo/ajax/photo/' + photoPk + '/' + likeType + '/';
    // console.log(url);
    $.ajax({
        method: 'POST',
        url: url,
    })
        .done(function(response, textStatus) {
            console.log(response);
            var likeCount = response.like_count;
            var dislikeCount = response.dislike_count;
            var userLike = response.user_like;
            var userDislike = response.user_dislike;

            var spanLikeCount = $('#photo-' + photoPk + '-like-count');
            var spanDislikeCount = $('#photo-' + photoPk + '-dislike-count');
            spanLikeCount.text(likeCount);
            spanDislikeCount.text(dislikeCount);

            var btnLike = $('#btn-photo-' + photoPk + '-like');
            var btnDislike = $('#btn-photo-' + photoPk + '-dislike');
            if(userLike) {
                btnLike.addClass('label-info');
                btnLike.removeClass('label-default');
            } else {
                btnLike.removeClass('label-info');
                btnLike.addClass('label-default');
            }
            if(userDislike) {
                btnDislike.addClass('label-danger');
                btnDislike.removeClass('label-default');
            } else {
                btnDislike.removeClass('label-danger');
                btnDislike.addClass('label-default');
            }
        })
        .fail(function(response, textStatus) {
            console.log(response);
        });
}