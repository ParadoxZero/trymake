/**
 * Created by Bineeth on 30-06-2017.
 */

(function(){

    var app = angular.module('login', []).config(function ($httpProvider) {
        $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });
    var loginEmail = function ($scope, $http) {
        $scope.check_mail = function (email) {
            var param = {
                'email' : email
            };

            var onSuccess = function (responce) {
                $scope.user = responce.data;
            };
            var onReject = function (error) {
                $scope.error = "no email exists";
            };
            $http.post('/check_account' , param)
                .then(onSuccess , onReject);
        };



    };
    app.controller('loginEmail' ,  loginEmail);

}());