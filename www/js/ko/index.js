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
    bootstrap: 'bootstrap.min',
    crypto: 'crypto.core',
    'crypto.SHA': 'sha256'
  },
  shim: {
    'crypto.SHA' : ['crypto']
  }
});

requirejs(['jquery', 'knockout', 'kopunches', 'kofilebind', 'pager', 'jqueryvalidate', 'bootbox', 'bootstrap', 'crypto.SHA'], function($, ko, kopunches, kofilebind, pager, $valid, bootbox, bootstrap, crypt) {
  function RootViewModel() {
    var self = this;
    self.search = ko.observable("");
    self.loginState = ko.observable('unregistered');
    self.username = ko.observable("");

    self.onSearchClick = function() {
      if (self.search() === "") {
        window.location.assign("/#!/");
      } else {
        window.location.assign("/#!/publications?search="+encodeURIComponent(self.search()));
      }
    };
    self.loginModal = function() {
      bootbox.dialog({
        message: '<form id="loginModal" submit="" data-bind="submit: loginUser"></form>',
        title: "Login",
        show: true,
        backdrop: true,
        closeButton: true,
        animate: true,
        className: "my-modal",
        buttons: {
          success: {
            label: "Login",
            className: "btn-success",
            callback: loginUser
          },
          danger: {
            label: "Cancel",
            className: "btn-danger"
          }
        }
      });
      $('#loginModal').load('views/loginModal.html');
    };
    self.logout = function() {
      self.loginState('unregistered');
      window.location.assign("/");
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

  function loginUser(result) {
    var username = $('#username').val();
    var password = CryptoJS.SHA256($('#password').val());
    if(username && password) {

      var loginObject = {
        username: username,
        hash: password.toString()
      };

      $.get('/api/login.py', loginObject)
      .done(function(data) {
        rootViewModel.loginState(data.Permission);
        rootViewModel.username(username);
      })
      .error(function (jqXHR) {
        rootViewModel.loginState('unregistered');
        bootbox.dialog({
          message: "Error (" + jqXHR.status + ") " + jqXHR.statusText,
          title: "Error Uploading",
          buttons: {
            'OK': {
              className: "btn-success"
            }
          }});
        });
      }

    }
  });
