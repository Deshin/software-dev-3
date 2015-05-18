requirejs.config({
  baseUrl: 'js',
  urlArgs: "bust=" + (new Date()).getTime(),
  paths: {
    jquery: 'jquery-2.1.3.min',
    jqueryvalidate: 'jquery.validate.min',
    knockout: 'knockout-3.3.0',
    kopunches: 'knockout.punches.min',
    pager: 'pager.min'
  }
});

requirejs(['jquery', 'knockout', 'kopunches', 'pager', 'jqueryvalidate'], function($, ko, kopunches, pager, $valid) {
  function RootViewModel() {
    var self = this;
    self.search = ko.observable("");
    self.onSearchClick = function() {
      if (self.search() === "") {
        window.location.assign("/");
      } else {
        window.location.assign("/#!/publications?search="+encodeURIComponent(self.search()));
      }
    };
    self.getVM = function(path) {
      return function(callback) {
        requirejs(['/js/ko/viewmodels/'+path+'.js'], function(mod) {
          callback(mod);
        });
      };
    };
  }

  rootViewModel = new RootViewModel();

  pager.Href.hash = '#!/';

  pager.extendWithPage(rootViewModel);

  ko.punches.enableAll();

  ko.applyBindings(rootViewModel);

  pager.start();
});
