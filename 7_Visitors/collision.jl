abstract type Object end

struct Car <: Object end
struct Wall <: Object end

function collide(a::Object, b::Object)
    println("Calling dispatch")
    _collide(a, b)
end

_collide(a::Car, b::Car) = println("Two cars collided")
_collide(a::Car, b::Wall) = println("Car hit wall")
_collide(a::Wall, b::Car) = println("Wall hit car")
_collide(a::Wall, b::Wall) = println("Two walls collided")

collide(Car(), Wall())
