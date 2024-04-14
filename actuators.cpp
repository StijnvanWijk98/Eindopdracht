#include <pybind11/pybind11.h>
#include <iostream>

namespace py = pybind11;

class Actuator{
    protected:
        bool state;
    public:
        Actuator() : state(false) {}

        virtual void on(){
            state = true;
        }

        virtual void off(){
            state = false;
        }

        virtual bool getState() const{
            return state;
        }
};

class BrakeActuator : public Actuator{
    private:
        unsigned int brakePressure;
    public:
        BrakeActuator() : brakePressure(0) {Actuator();}

        void setPressure(unsigned int pressure){
            if (pressure > 0){
                Actuator::on();
            } else {
                Actuator::off();
            }
            if (pressure > 100) pressure = 100;
            brakePressure = pressure;
            std::cout << "Brake pressure set to " << brakePressure << std::endl;
        }

        unsigned int getPressure() const{
            return brakePressure;
        }

        void on() override{
            Actuator::on();
            brakePressure = 100;
            std::cout << "Brake actuator turned on" << std::endl;
        }

        void off() override{
            Actuator::off();
            brakePressure = 0;
            std::cout << "Brake actuator turned off" << std::endl;
        }
};

class ThrottleActuator : public Actuator{
    private:
        unsigned int throttlePosition;
    public:
        ThrottleActuator() : throttlePosition(0) {Actuator();}

        void setPosition(unsigned int position){
            if (position > 0){
                Actuator::on();
            } else {
                Actuator::off();
            }
            if (position > 100) position = 100;
            throttlePosition = position;
            std::cout << "Throttle position set to " << throttlePosition << std::endl;
        }

        unsigned int getPosition() const{
            return throttlePosition;
        }

        void on() override{
            Actuator::on();
            throttlePosition = 100;
            std::cout << "Throttle actuator turned on" << std::endl;
        }

        void off() override{
            Actuator::off();
            throttlePosition = 0;
            std::cout << "Throttle actuator turned off" << std::endl;
        }
};


PYBIND11_MODULE(actuators, m) {
    pybind11::class_<Actuator>(m, "Actuator")
        .def(pybind11::init<>())
        .def("on", &Actuator::on)
        .def("off", &Actuator::off)
        .def("get_state", &Actuator::getState);

    pybind11::class_<BrakeActuator, Actuator>(m, "BrakeActuator")
        .def(pybind11::init<>())
        .def("set_pressure", &BrakeActuator::setPressure)
        .def("get_pressure", &BrakeActuator::getPressure)
        .def("on", &BrakeActuator::on)
        .def("off", &BrakeActuator::off);
    
    pybind11::class_<ThrottleActuator, Actuator>(m, "ThrottleActuator")
        .def(pybind11::init<>())
        .def("set_position", &ThrottleActuator::setPosition)
        .def("get_position", &ThrottleActuator::getPosition)
        .def("on", &ThrottleActuator::on)
        .def("off", &ThrottleActuator::off);
}