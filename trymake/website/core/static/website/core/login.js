/*
Author: Bineeth (bineeth@trymake.com)

Copyright (c) 2017 Sibibia Technologies Pvt Ltd
All Rights Reserved

Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
 */

(function(){

    var app = angular.module('login', [], function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}')
    }).config(function ($httpProvider) {
        $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });
    var loginEmail = function ($scope, $http , $window) {
            //Checks for email
        $scope.check_mail = function (email) {
            var param ="email=" + email;

            var onSuccess = function (responce) {
                $scope.user = responce.data;
            };
            var onReject = function (error) {
                $scope.error = "no email exists";
            };
            $http({
                method  : 'POST',
                url     : '/check_account',
                data    : param,
                headers : {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(onSuccess , onReject);
        };
            //Authenticates the user
        $scope.login = function (email , password) {
            var param = "email="+$scope.email+"&password="+$scope.password;
            var onSuccess = function (response) {
                $scope.msg = "successfully logged in";
                //For development purposes only
                //$window.location.href = '/account/';
                console.log(response.data)
            };
            var onReject = function (error) {
                $scope.error = "Incorrect password";
            };
            $http({
                method  : 'POST',
                url     : '/login',
                data    : param,
                headers : {'Content-Type': 'application/x-www-form-urlencoded'}
            })
                .then(onSuccess , onReject);
        };
            // If no user available when email id is entered then register form is shown
        $scope.register = function () {
            var param = "name="+$scope.name+"&phone="+$scope.phone
                    +"&email="+$scope.email+"&password="+$scope.password
                    +"&password_verify="+$scope.password_verify;
            var onSuccess = function (response) {
                $scope.reg = response.data;
                console.log($scope.reg);
                if($scope.reg.status === 'ok'){
                    $scope.user = null;
                    $scope.name = $scope.phone = $scope.email =
                        $scope.password = $scope.password_verify = null;
                }
            };
            var onError = function (error) {
                $scope.error = "Something went wrong.. Try again"
            };
            $http({
                method  : 'POST',
                url     : '/process_registration',
                data    : param,
                headers : {'Content-Type': 'application/x-www-form-urlencoded'}
            }).then(onSuccess , onError);
        };

    };
    app.controller('loginEmail' ,  loginEmail);

}());
