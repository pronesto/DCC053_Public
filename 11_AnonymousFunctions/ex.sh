#!/bin/bash

foo() {
    echo $x
}

bar() {
    local x=10
    foo
}

x=5
bar
