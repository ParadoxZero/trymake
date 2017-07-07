/*
*   Author: Bineeth (bineeth@trymake.com)
*
*   Copyright (c) 2017 Sibibia Technologies Pvt Ltd
*   All Rights Reserved
*
*   Unauthorized copying of this file, via any medium is strictly prohibited
*   Proprietary and confidential
 */
(function () {
    'use strict';

    var module = angular.module('angular-bind-html-compile', []);

    module.directive('bindHtmlCompile', ['$compile', function ($compile) {
        return {
            restrict: 'A',
            link: function (scope, element, attrs) {
                scope.$watch(function () {
                    return scope.$eval(attrs.bindHtmlCompile);
                }, function (value) {
                    element.html(value);
                    $compile(element.contents())(scope);
                });
            }
        };
    }]);
}());