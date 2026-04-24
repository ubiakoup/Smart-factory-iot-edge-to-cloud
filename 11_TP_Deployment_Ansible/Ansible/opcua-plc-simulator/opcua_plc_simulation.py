from opcua import Server
import random
import datetime
import time
import threading
import math


# ===============================
# Global variables
# ===============================

mode = "normal"
stop_event = threading.Event()

print("Select the simulation mode | Choisissez le mode de simulation:")
print("n → Normal simulation")
print("f → Progressive system failure")
print("b → Bearing failure simulation")
print("q → Stop the server")

choice = input("Your choice | Votre choix : ").strip().lower()

if choice == "n":
    mode = "normal"

elif choice == "f":
    mode = "fault"

elif choice == "b":
    mode = "bearing"

elif choice == "q":
    exit()

else:
    mode = "normal"


# ===============================
# Keyboard listener
# ===============================

def keyboard_listener():
    global mode

    while not stop_event.is_set():
        try:
            cmd = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            stop_event.set()
            break

        if cmd == "n":
            mode = "normal"
            print("🟢 Mode NORMAL activé")

        elif cmd == "f":
            mode = "fault"
            print("🔴 Mode PANNE activé")
        
        elif cmd == "b":
            mode = "bearing"
            print("⚠ BEARING FAILURE MODE activé")

        elif cmd == "q":
            print("🛑 Arrêt du serveur demandé")
            stop_event.set()


# ===============================
# Creating OPC UA Server
# ===============================

server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840")

name = "OPCUA_SERVER_PLC_SIMULATION"
idx = server.register_namespace(name)

objects = server.get_objects_node()

# ===============================
# PLC1 : Motor System
# ===============================

plc1 = objects.add_object(idx, "PLC1_Motor_System")

temp_motor = plc1.add_variable("ns=2;s=plc1.temperature", "Temperature", 40.0)
vibration_motor = plc1.add_variable("ns=2;s=plc1.vibration", "Vibration", 0.5)
motor_current = plc1.add_variable("ns=2;s=plc1.motor_current", "MotorCurrent", 8.0)
motor_speed = plc1.add_variable("ns=2;s=plc1.motor_speed", "MotorSpeed", 1500)
bearing_health = plc1.add_variable("ns=2;s=plc1.bearing_health", "BearingHealth", 100.0)
Time_1 = plc1.add_variable("ns=2;s=plc1.time", "Time", "")

# ===============================
# PLC2 : Hydraulic System
# ===============================

plc2 = objects.add_object(idx, "PLC2_Hydraulic_System")

hydraulic_pressure = plc2.add_variable("ns=2;s=plc2.pressure", "Pressure", 120.0)
hydraulic_temp = plc2.add_variable("ns=2;s=plc2.temperature", "Temperature", 50.0)
flow_rate = plc2.add_variable("ns=2;s=plc2.flow_rate", "FlowRate", 20.0)
oil_level = plc2.add_variable("ns=2;s=plc2.oil_level", "OilLevel", 100.0)
Time_2 = plc2.add_variable("ns=2;s=plc2.time", "Time", "")

# ===============================
# PLC3 : Energy Monitoring
# ===============================

plc3 = objects.add_object(idx, "PLC3_Energy_Monitoring")

voltage = plc3.add_variable("ns=2;s=plc3.voltage", "Voltage", 230.0)
current = plc3.add_variable("ns=2;s=plc3.current", "Current", 12.0)
energy = plc3.add_variable("ns=2;s=plc3.energy", "EnergyConsumption", 500.0)
power_factor = plc3.add_variable("ns=2;s=plc3.power_factor", "PowerFactor", 0.95)
Time_3 = plc3.add_variable("ns=2;s=plc3.time", "Time", "")

# ===============================
# Allow writing
# ===============================

variables = [
    temp_motor,
    vibration_motor,
    motor_current,
    motor_speed,
    bearing_health,
    Time_1,
    hydraulic_pressure,
    hydraulic_temp,
    flow_rate,
    oil_level,
    Time_2,
    voltage,
    current,
    energy,
    power_factor,
    Time_3
]

for var in variables:
    var.set_writable()

# ===============================
# Failure simulation variable
# ===============================

fault_counter = 0
time_counter = 0

# ===============================
# Start keyboard listener thread
# ===============================

thread = threading.Thread(target=keyboard_listener, daemon=True)
thread.start()

# ===============================
# Start OPC UA Server
# ===============================

server.start()

print("🚀 OPC UA Server started : opc.tcp://192.168.56.11:4840")
print("Commands: n = normal | f = failure | q = stop")

# ===============================
# Main Simulation Loop
# ===============================

temp_motor_value = 40
vibration_value = 0.35
motor_current_value = 8
motor_speed_value = 1500

hydraulic_pressure_value = 130
hydraulic_temp_value = 40
flow_rate_value = 21
oil_level_value = 95

voltage_value = 230
current_value = 12
energy_value = 480
power_factor_value = 0.95
bearing_health_value = 98

try:

    while not stop_event.is_set():

        now = str(datetime.datetime.now())

        # ===========================
        # NORMAL MODE
        # ===========================

        if mode == "normal":

            
            # MOTOR SYSTEM

            temp_motor_value += random.uniform(-0.3,0.3)
            temp_motor_value = max(35, min(48, temp_motor_value))

            vibration_value += random.uniform(-0.02,0.02)
            vibration_value = max(0.2, min(0.6, vibration_value))

            motor_current_value += random.uniform(-0.1,0.1)
            motor_current_value = max(7, min(9, motor_current_value))

            motor_speed_value += random.uniform(-5,5)
            motor_speed_value = max(1480, min(1520, motor_speed_value))

            bearing_health_value += random.uniform(-0.05,0.05)
            bearing_health_value = max(96, min(100, bearing_health_value))


            # HYDRAULIC SYSTEM

            hydraulic_pressure_value += random.uniform(-1,1)
            hydraulic_pressure_value = max(120, min(140, hydraulic_pressure_value))

            hydraulic_temp_value += random.uniform(-0.3,0.3)
            hydraulic_temp_value = max(35, min(45, hydraulic_temp_value))

            flow_rate_value += random.uniform(-0.3,0.3)
            flow_rate_value = max(19, min(23, flow_rate_value))

            oil_level_value += random.uniform(-0.1,0.1)
            oil_level_value = max(90, min(100, oil_level_value))


            # ENERGY SYSTEM

            voltage_value += random.uniform(-1,1)
            voltage_value = max(225, min(235, voltage_value))

            current_value += random.uniform(-0.2,0.2)
            current_value = max(10, min(13, current_value))

            energy_value += random.uniform(-5,5)
            energy_value = max(420, min(520, energy_value))

            power_factor_value += random.uniform(-0.01,0.01)
            power_factor_value = max(0.92, min(0.98, power_factor_value))


            # APPLY VALUES

            temp_motor.set_value(round(temp_motor_value,2))
            vibration_motor.set_value(round(vibration_value,2))
            motor_current.set_value(round(motor_current_value,2))
            motor_speed.set_value(round(motor_speed_value,2))
            bearing_health.set_value(round(bearing_health_value,2))

            hydraulic_pressure.set_value(round(hydraulic_pressure_value,2))
            hydraulic_temp.set_value(round(hydraulic_temp_value,2))
            flow_rate.set_value(round(flow_rate_value,2))
            oil_level.set_value(round(oil_level_value,2))

            voltage.set_value(round(voltage_value,2))
            current.set_value(round(current_value,2))
            energy.set_value(round(energy_value,2))
            power_factor.set_value(round(power_factor_value,2))

        # ===========================
        # FAILURE MODE
        # ===========================

        elif mode == "fault":
    
            # MOTOR SYSTEM

            temp_motor_value += random.uniform(0.2,0.6)
            temp_motor_value = min(90, temp_motor_value)

            vibration_value += random.uniform(0.05,0.15)
            vibration_value = min(4, vibration_value)

            motor_current_value += random.uniform(0.1,0.3)
            motor_current_value = min(15, motor_current_value)

            motor_speed_value += random.uniform(-15,5)
            motor_speed_value = max(1200, min(1500, motor_speed_value))

            bearing_health_value -= random.uniform(0.5,1.5)
            bearing_health_value = max(0, bearing_health_value)


            # HYDRAULIC SYSTEM

            hydraulic_pressure_value += random.uniform(-3,1)
            hydraulic_pressure_value = max(80, min(140, hydraulic_pressure_value))

            hydraulic_temp_value += random.uniform(0.3,0.8)
            hydraulic_temp_value = min(70, hydraulic_temp_value)

            flow_rate_value += random.uniform(-0.8,-0.2)
            flow_rate_value = max(10, flow_rate_value)

            oil_level_value += random.uniform(-0.5,-0.1)
            oil_level_value = max(50, oil_level_value)


            # ENERGY SYSTEM

            voltage_value += random.uniform(-2,2)
            voltage_value = max(210, min(240, voltage_value))

            current_value += random.uniform(0.3,0.8)
            current_value = min(20, current_value)

            energy_value += random.uniform(10,25)
            energy_value = min(900, energy_value)

            power_factor_value -= random.uniform(0.01,0.03)
            power_factor_value = max(0.6, power_factor_value)

            if vibration_value > 3:
             print("⚠ CRITICAL MACHINE VIBRATION")

            if temp_motor_value > 80:
             print("🔥 MOTOR OVERHEATING")

            if bearing_health_value < 30:
             print("🚨 BEARING FAILURE")


            # APPLY VALUES

            temp_motor.set_value(round(temp_motor_value,2))
            vibration_motor.set_value(round(vibration_value,2))
            motor_current.set_value(round(motor_current_value,2))
            motor_speed.set_value(round(motor_speed_value,2))
            bearing_health.set_value(round(bearing_health_value,2))

            hydraulic_pressure.set_value(round(hydraulic_pressure_value,2))
            hydraulic_temp.set_value(round(hydraulic_temp_value,2))
            flow_rate.set_value(round(flow_rate_value,2))
            oil_level.set_value(round(oil_level_value,2))

            voltage.set_value(round(voltage_value,2))
            current.set_value(round(current_value,2))
            energy.set_value(round(energy_value,2))
            power_factor.set_value(round(power_factor_value,2))

        # ===========================
        # Bearing MODE
        # =========================== 
        elif mode == "bearing":
    
            # MOTOR SYSTEM (bearing degradation)

            temp_motor_value += random.uniform(0.2,0.5)
            temp_motor_value = min(90, temp_motor_value)

            vibration_value += random.uniform(0.15,0.35)
            vibration_value = min(5, vibration_value)

            motor_current_value += random.uniform(0.1,0.25)
            motor_current_value = min(14, motor_current_value)

            motor_speed_value += random.uniform(-10,10)
            motor_speed_value = max(1300, min(1500, motor_speed_value))

            bearing_health_value -= random.uniform(1,3)
            bearing_health_value = max(0, bearing_health_value)


            # HYDRAULIC SYSTEM (mostly stable)

            hydraulic_pressure_value += random.uniform(-1,1)
            hydraulic_pressure_value = max(120, min(140, hydraulic_pressure_value))

            hydraulic_temp_value += random.uniform(-0.2,0.3)
            hydraulic_temp_value = max(35, min(45, hydraulic_temp_value))

            flow_rate_value += random.uniform(-0.2,0.2)
            flow_rate_value = max(19, min(23, flow_rate_value))

            oil_level_value += random.uniform(-0.05,0.05)
            oil_level_value = max(90, min(100, oil_level_value))


            # ENERGY SYSTEM (motor consumes more)

            voltage_value += random.uniform(-1,1)
            voltage_value = max(220, min(240, voltage_value))

            current_value += random.uniform(0.2,0.6)
            current_value = min(18, current_value)

            energy_value += random.uniform(8,20)
            energy_value = min(900, energy_value)

            power_factor_value -= random.uniform(0.005,0.02)
            power_factor_value = max(0.7, power_factor_value)

            if vibration_value > 3:
                print("⚠ BEARING FAILURE DETECTED")


            # APPLY VALUES

            temp_motor.set_value(round(temp_motor_value,2))
            vibration_motor.set_value(round(vibration_value,2))
            motor_current.set_value(round(motor_current_value,2))
            motor_speed.set_value(round(motor_speed_value,2))
            bearing_health.set_value(round(bearing_health_value,2))

            hydraulic_pressure.set_value(round(hydraulic_pressure_value,2))
            hydraulic_temp.set_value(round(hydraulic_temp_value,2))
            flow_rate.set_value(round(flow_rate_value,2))
            oil_level.set_value(round(oil_level_value,2))

            voltage.set_value(round(voltage_value,2))
            current.set_value(round(current_value,2))
            energy.set_value(round(energy_value,2))
            power_factor.set_value(round(power_factor_value,2))
            

        # ===========================
        # Update timestamps
        # ===========================

        Time_1.set_value(now)
        Time_2.set_value(now)
        Time_3.set_value(now)

        # ===========================
        # Display sensor values
        # ===========================

        print("\n================ Industrial Data =================")

        print(f"[PLC1 - Motor System]")
        print(f"Temperature      : {temp_motor.get_value()} °C")
        print(f"Vibration        : {vibration_motor.get_value()} g")
        print(f"Motor Current    : {motor_current.get_value()} A")
        print(f"Motor Speed      : {motor_speed.get_value()} RPM")
        print(f"bearing health   : {bearing_health.get_value()} %")

        print(f"\n[PLC2 - Hydraulic System]")
        print(f"Pressure         : {hydraulic_pressure.get_value()} bar")
        print(f"Temperature      : {hydraulic_temp.get_value()} °C")
        print(f"flow_rate        : {flow_rate.get_value()} L/min")
        print(f"oil_level        : {oil_level.get_value()} %")

        print(f"\n[PLC3 - Energy Monitoring]")
        print(f"Voltage          : {voltage.get_value()} V")
        print(f"Current          : {current.get_value()} A")
        print(f"Energy           : {energy.get_value()} W")
        print(f"power_factor     : {power_factor.get_value()}")

        print(f"\nTimestamp        : {now}")
        print("=================================================\n")

        time.sleep(2)

finally:

    server.stop()

    print("🛑 OPC UA Server stopped successfully")