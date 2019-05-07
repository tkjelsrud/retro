function loadBoard(id, key) {
  $.ajax({
        url: '/retro/node/' + id + '?s=' + key,
        dataType: 'json',
        cache: false
    }).done(function(data){
      console.log(data);
    //for(i = 0; i < data['notes'].length; i++) {
    //        nd = data['notes'][i];
    //        DrawNote(nd);
    //}
  });
}

function loadBoardElements(id) {
  $.ajax({
        url: '/retro/node/' + id + '/children',
        dataType: 'json',
        cache: false
    }).done(function(data){
      alert(data);
    //for(i = 0; i < data['notes'].length; i++) {
    //        nd = data['notes'][i];
    //        DrawNote(nd);
    //}
  });
}
