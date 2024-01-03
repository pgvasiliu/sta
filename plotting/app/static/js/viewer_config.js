window.addEventListener('DOMContentLoaded', function () {
  var galley = document.getElementById('galley');
  var viewer = new Viewer(galley, {
    url: 'src',
    title: function (image) {
      return image.alt + ' (' + (this.index + 1) + '/' + this.length + ')';
    },
  });
});
