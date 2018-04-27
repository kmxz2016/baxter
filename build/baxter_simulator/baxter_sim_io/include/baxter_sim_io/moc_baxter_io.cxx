/****************************************************************************
** Meta object code from reading C++ file 'baxter_io.hpp'
**
** Created by: The Qt Meta Object Compiler version 63 (Qt 4.8.6)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "../../../../../src/baxter_simulator/baxter_sim_io/include/baxter_sim_io/baxter_io.hpp"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'baxter_io.hpp' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 63
#error "This file was generated using the moc from 4.8.6. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_baxter_sim_io__BaxterIO[] = {

 // content:
       6,       // revision
       0,       // classname
       0,    0, // classinfo
      40,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       0,       // signalCount

 // slots: signature, parameters, type, tag, flags
      25,   24,   24,   24, 0x08,
      50,   24,   24,   24, 0x08,
      76,   24,   24,   24, 0x08,
     105,   24,   24,   24, 0x08,
     144,  135,   24,   24, 0x08,
     178,   24,   24,   24, 0x08,
     205,   24,   24,   24, 0x08,
     233,   24,   24,   24, 0x08,
     264,   24,   24,   24, 0x08,
     296,   24,   24,   24, 0x08,
     322,   24,   24,   24, 0x08,
     349,   24,   24,   24, 0x08,
     378,   24,   24,   24, 0x08,
     408,   24,   24,   24, 0x08,
     438,   24,   24,   24, 0x08,
     469,   24,   24,   24, 0x08,
     503,   24,   24,   24, 0x08,
     538,   24,   24,   24, 0x08,
     570,   24,   24,   24, 0x08,
     603,  135,   24,   24, 0x08,
     642,   24,   24,   24, 0x08,
     673,   24,   24,   24, 0x08,
     705,   24,   24,   24, 0x08,
     740,   24,   24,   24, 0x08,
     776,  135,   24,   24, 0x08,
     816,   24,   24,   24, 0x08,
     849,   24,   24,   24, 0x08,
     883,   24,   24,   24, 0x08,
     909,   24,   24,   24, 0x08,
     936,   24,   24,   24, 0x08,
     966,   24,   24,   24, 0x08,
     997,  135,   24,   24, 0x08,
    1032,   24,   24,   24, 0x08,
    1060,   24,   24,   24, 0x08,
    1089,   24,   24,   24, 0x08,
    1121,   24,   24,   24, 0x08,
    1154,   24,   24,   24, 0x08,
    1181,   24,   24,   24, 0x08,
    1209,   24,   24,   24, 0x08,
    1239,   24,   24,   24, 0x08,

       0        // eod
};

static const char qt_meta_stringdata_baxter_sim_io__BaxterIO[] = {
    "baxter_sim_io::BaxterIO\0\0"
    "on_left_arm_ok_pressed()\0"
    "on_left_arm_ok_released()\0"
    "on_left_arm_cancel_pressed()\0"
    "on_left_arm_cancel_released()\0position\0"
    "on_left_arm_dial_sliderMoved(int)\0"
    "on_left_arm_show_pressed()\0"
    "on_left_arm_show_released()\0"
    "on_left_cuff_squeeze_pressed()\0"
    "on_left_cuff_squeeze_released()\0"
    "on_left_cuff_ok_pressed()\0"
    "on_left_cuff_ok_released()\0"
    "on_left_cuff_grasp_pressed()\0"
    "on_left_cuff_grasp_released()\0"
    "on_left_shoulder_ok_pressed()\0"
    "on_left_shoulder_ok_released()\0"
    "on_left_shoulder_cancel_pressed()\0"
    "on_left_shoulder_cancel_released()\0"
    "on_left_shoulder_show_pressed()\0"
    "on_left_shoulder_show_released()\0"
    "on_left_shoulder_dial_sliderMoved(int)\0"
    "on_right_shoulder_ok_pressed()\0"
    "on_right_shoulder_ok_released()\0"
    "on_right_shoulder_cancel_pressed()\0"
    "on_right_shoulder_cancel_released()\0"
    "on_right_shoulder_dial_sliderMoved(int)\0"
    "on_right_shoulder_show_pressed()\0"
    "on_right_shoulder_show_released()\0"
    "on_right_arm_ok_pressed()\0"
    "on_right_arm_ok_released()\0"
    "on_right_arm_cancel_pressed()\0"
    "on_right_arm_cancel_released()\0"
    "on_right_arm_dial_sliderMoved(int)\0"
    "on_right_arm_show_pressed()\0"
    "on_right_arm_show_released()\0"
    "on_right_cuff_squeeze_pressed()\0"
    "on_right_cuff_squeeze_released()\0"
    "on_right_cuff_ok_pressed()\0"
    "on_right_cuff_ok_released()\0"
    "on_right_cuff_grasp_pressed()\0"
    "on_right_cuff_grasp_released()\0"
};

void baxter_sim_io::BaxterIO::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        Q_ASSERT(staticMetaObject.cast(_o));
        BaxterIO *_t = static_cast<BaxterIO *>(_o);
        switch (_id) {
        case 0: _t->on_left_arm_ok_pressed(); break;
        case 1: _t->on_left_arm_ok_released(); break;
        case 2: _t->on_left_arm_cancel_pressed(); break;
        case 3: _t->on_left_arm_cancel_released(); break;
        case 4: _t->on_left_arm_dial_sliderMoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 5: _t->on_left_arm_show_pressed(); break;
        case 6: _t->on_left_arm_show_released(); break;
        case 7: _t->on_left_cuff_squeeze_pressed(); break;
        case 8: _t->on_left_cuff_squeeze_released(); break;
        case 9: _t->on_left_cuff_ok_pressed(); break;
        case 10: _t->on_left_cuff_ok_released(); break;
        case 11: _t->on_left_cuff_grasp_pressed(); break;
        case 12: _t->on_left_cuff_grasp_released(); break;
        case 13: _t->on_left_shoulder_ok_pressed(); break;
        case 14: _t->on_left_shoulder_ok_released(); break;
        case 15: _t->on_left_shoulder_cancel_pressed(); break;
        case 16: _t->on_left_shoulder_cancel_released(); break;
        case 17: _t->on_left_shoulder_show_pressed(); break;
        case 18: _t->on_left_shoulder_show_released(); break;
        case 19: _t->on_left_shoulder_dial_sliderMoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 20: _t->on_right_shoulder_ok_pressed(); break;
        case 21: _t->on_right_shoulder_ok_released(); break;
        case 22: _t->on_right_shoulder_cancel_pressed(); break;
        case 23: _t->on_right_shoulder_cancel_released(); break;
        case 24: _t->on_right_shoulder_dial_sliderMoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 25: _t->on_right_shoulder_show_pressed(); break;
        case 26: _t->on_right_shoulder_show_released(); break;
        case 27: _t->on_right_arm_ok_pressed(); break;
        case 28: _t->on_right_arm_ok_released(); break;
        case 29: _t->on_right_arm_cancel_pressed(); break;
        case 30: _t->on_right_arm_cancel_released(); break;
        case 31: _t->on_right_arm_dial_sliderMoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 32: _t->on_right_arm_show_pressed(); break;
        case 33: _t->on_right_arm_show_released(); break;
        case 34: _t->on_right_cuff_squeeze_pressed(); break;
        case 35: _t->on_right_cuff_squeeze_released(); break;
        case 36: _t->on_right_cuff_ok_pressed(); break;
        case 37: _t->on_right_cuff_ok_released(); break;
        case 38: _t->on_right_cuff_grasp_pressed(); break;
        case 39: _t->on_right_cuff_grasp_released(); break;
        default: ;
        }
    }
}

const QMetaObjectExtraData baxter_sim_io::BaxterIO::staticMetaObjectExtraData = {
    0,  qt_static_metacall 
};

const QMetaObject baxter_sim_io::BaxterIO::staticMetaObject = {
    { &QMainWindow::staticMetaObject, qt_meta_stringdata_baxter_sim_io__BaxterIO,
      qt_meta_data_baxter_sim_io__BaxterIO, &staticMetaObjectExtraData }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &baxter_sim_io::BaxterIO::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *baxter_sim_io::BaxterIO::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *baxter_sim_io::BaxterIO::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_baxter_sim_io__BaxterIO))
        return static_cast<void*>(const_cast< BaxterIO*>(this));
    return QMainWindow::qt_metacast(_clname);
}

int baxter_sim_io::BaxterIO::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QMainWindow::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 40)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 40;
    }
    return _id;
}
QT_END_MOC_NAMESPACE
