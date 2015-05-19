requirejs.config({
  baseUrl: 'js',
  urlArgs: "bust=" + (new Date()).getTime(),
  paths: {
    jquery: 'jquery-2.1.3.min',
    jqueryvalidate: 'jquery.validate.min',
    knockout: 'knockout-3.3.0',
    kopunches: 'knockout.punches.min',
    kofilebind: 'knockout-file-bindings',
    pager: 'pager.min',
    bootbox: 'bootbox.min',
    bootstrap: 'bootstrap.min'
  }
});

requirejs(['jquery', 'knockout', 'kopunches', 'kofilebind', 'pager', 'jqueryvalidate', 'bootbox', 'bootstrap'], function($, ko, kopunches, kofilebind, pager, $valid, bootbox, bootstrap) {
  function RootViewModel() {
    var self = this;
    self.search = ko.observable("");
    self.username = ko.observable("");
    self.password = ko.observable("");
    self.onSearchClick = function() {
      if (self.search() === "") {
        window.location.assign("/");
      } else {
        window.location.assign("/#!/publications?search="+encodeURIComponent(self.search()));
      }
    };
    self.loginModal = function() {
      bootbox.dialog({
        message: '<form id="loginModal"></form>',
        title: "Custom title",
        show: true,
        backdrop: true,
        closeButton: true,
        animate: true,
        className: "my-modal",
        buttons: {
          "Confirm": {
            className: "btn-success",
            callback: loginUser
          },
          "Cancel": {
            className: "btn-danger"
          }
        }
      });
      $('#loginModal').load('views/loginModal.html');

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

  function loginUser() {
    var username = $('#username').val();
    var password = $('#password').val();
    if(username && password) {
      console.log(username);
      console.log(username);
    }

  }
});
