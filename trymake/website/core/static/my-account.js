/**
 * Created by Bineeth on 03-07-2017.
 */
(function () {
    var app = angular.module('my_account' , [] , function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}')
    }).config(function ($httpProvider) {
        $httpProvider.defaults.headers.post['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    });

    var get_order = function ($scope , $http) {
        $scope.view_orders = function (get_list) {
            var url = 'ajax/orders/get';
            var onSuccess = function (responce) {
                $scope.return_list = responce.data;
            };
            var onReject = function () {
                $scope.return_list = "Something went worng.. Try again!"
            };
            $http.get(url,get_list).then(onSuccess , onReject);
        };
    };
    app.controller('get_order' ,  get_order);

}());

