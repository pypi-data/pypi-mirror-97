/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

export default class FormatUtils {
    public static msToTime(s: number) {
        var ms = s % 1000;
        s = (s - ms) / 1000;
        var secs = s % 60;
        s = (s - secs) / 60;
        var mins = s % 60;
        var hrs = (s - mins) / 60;
    
        return (hrs == 0 ? '' : (hrs < 10 ? '0' + hrs : hrs) + ':') + (mins < 10 ? '0' + mins : mins) + ':' + (secs < 10 ? '0' + secs : secs)/* + '.' + ms*/;
    }

    public static styleCapacityUnit() {
        return (value: number): string => {
            if (value == -1) return ''
            if (value < Math.pow(1024, 3)) {
                return 'MiB';
            } else if (value < Math.pow(1024, 4)) {
                return 'GiB';
            } else if (value < Math.pow(1024, 5)) {
                return 'TiB';
            } else {
                return 'PiB';
            }
        };
    }
    
    public static styleCapacityValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < Math.pow(1024, 3)) {
                return (value / Math.pow(1024, 2)).toFixed(3);
            } else if (value < Math.pow(1024, 4)) {
                return (value / Math.pow(1024, 3)).toFixed(3);
            } else if (value < Math.pow(1024, 5)) {
                return (value / Math.pow(1024, 4)).toFixed(3);
            } else {
                return (value / Math.pow(1024, 5)).toFixed(3);
            }
        };
    }
    
    public static unstyleCapacityValue() {
        return (value: number, unit: string): number => {
            if (value == -1) return value
            if (isNaN(value)) return Number.NaN
            switch (unit.toLowerCase()) {
            case 'm':
            case 'mib':
                return value * Math.pow(1024, 2)
            case 'g':
            case 'gib':
                return value * Math.pow(1024, 3)
            case 't':
            case 'tib':
                return value * Math.pow(1024, 4)
            case 'p':
            case 'pib':
                return value * Math.pow(1024, 5)
            default:
                return value
            }
        }
    }
    
    public static styleCapacityUnitValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < Math.pow(1024, 2)) {
                return FormatUtils.customPrecision(value / Math.pow(1024, 1)) + ' KiB';
            } else if (value < Math.pow(1024, 3)) {
                return FormatUtils.customPrecision(value / Math.pow(1024, 2)) + ' MiB';
            } else if (value < Math.pow(1024, 4)) {
                return FormatUtils.customPrecision(value / Math.pow(1024, 3)) + ' GiB';
            } else if (value < Math.pow(1024, 5)) {
                return FormatUtils.customPrecision(value / Math.pow(1024, 4)) + ' TiB';
            } else {
                return FormatUtils.customPrecision(value / Math.pow(1024, 5)) + ' PiB';
            }
        };
    }
    
    // export function possibleCapacityUnitValue() {
    //     return (unitValue: string): boolean => {
    //         return unitValue.includes(/^(\d{1,4}|\d{1,2}\.\d|\d\.\d{2}) ?[mgtpezy]ib$/i)
    //     }
    // }
    
    // export function unstyleCapacityUnitValue() {
    //     return (unitValue: string): number => {
    //         if (unitValue == 'unsp') return -1
    //         var value: number = Number.parseFloat(unitValue.replace(/[^0-9\.]+/, ''))
    //         if (isNaN(value)) return Number.NaN
    //         var unit: string = unitValue.replace(/[0-9\.]+/, '').trim()
    //         switch (unit.toLowerCase()) {
    //         case 'mib':
    //             return value * Math.pow(1024, 2)
    //         case 'gib':
    //             return value * Math.pow(1024, 3)
    //         case 'tib':
    //             return value * Math.pow(1024, 4)
    //         case 'pib':
    //             return value * Math.pow(1024, 5)
    //         default:
    //             return Number.NaN
    //         }
    //     }
    // }
    
    public static styleThroughputUnit() {
        return (value: number): string => {
            if (value == -1) return ''
            if (value < Math.pow(1000, 3)) {
                return 'MBps';
            } else if (value < Math.pow(1000, 4)) {
                return 'GBps';
            } else if (value < Math.pow(1000, 5)) {
                return 'TBps';
            } else {
                return 'PiB';
            }
        };
    }
    
    public static styleThroughputValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < Math.pow(1000, 3)) {
                return (value / Math.pow(1000, 2)).toFixed(3);
            } else if (value < Math.pow(1000, 4)) {
                return (value / Math.pow(1000, 3)).toFixed(3);
            } else if (value < Math.pow(1000, 5)) {
                return (value / Math.pow(1000, 4)).toFixed(3);
            } else {
                return (value / Math.pow(1000, 5)).toFixed(3);
            }
        };
    }
    
    public static unstyleThroughputValue() {
        return (value: number, unit: string): number => {
            if (value == -1) return value
            if (isNaN(value)) return Number.NaN
            switch (unit.toLowerCase()) {
            case 'm':
            case 'mbps':
                return value * Math.pow(1000, 2)
            case 'g':
            case 'gbps':
                return value * Math.pow(1000, 3)
            case 't':
            case 'tbps':
                return value * Math.pow(1000, 4)
            case 'p':
            case 'pbps':
                return value * Math.pow(1000, 5)
            default:
                return value
            }
        }
    }
    
    public static styleThroughputUnitValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < Math.pow(1000, 3)) {
                return FormatUtils.customPrecision(value / Math.pow(1000, 2)) + ' MBps';
            } else if (value < Math.pow(1000, 4)) {
                return FormatUtils.customPrecision(value / Math.pow(1000, 3)) + ' GBps';
            } else if (value < Math.pow(1000, 5)) {
                return FormatUtils.customPrecision(value / Math.pow(1000, 4)) + ' TBps';
            } else {
                return FormatUtils.customPrecision(value / Math.pow(1000, 5)) + ' PBps';
            }
        };
    }
    
    // export function unstyleThroughputUnitValue() {
    //     return (unitValue: string): number => {
    //         if (unitValue == 'unsp') return -1
    //         var value: number = Number.parseFloat(unitValue.replace(/[^0-9\.]+/, ''))
    //         if (isNaN(value)) return Number.NaN
    //         var unit: string = unitValue.replace(/[0-9\.]+/, '').trim()
    //         switch (unit.toLowerCase()) {
    //         case 'mbps':
    //             return value * Math.pow(1000, 2)
    //         case 'gbps':
    //             return value * Math.pow(1000, 3)
    //         case 'tbps':
    //             return value * Math.pow(1000, 4)
    //         case 'pbps':
    //             return value * Math.pow(1000, 5)
    //         default:
    //             return Number.NaN
    //         }
    //     }
    // }
    
    public static styleFrequencyUnit() {
        return (value: number): string => {
            if (value == -1) return ''
            if (value < Math.pow(1000, 3)) {
                return 'MHz';
            } else if (value < Math.pow(1000, 4)) {
                return 'GHz';
            } else if (value < Math.pow(1000, 5)) {
                return 'THz';
            } else {
                return 'PHz';
            }
        };
    }
    
    public static styleFrequencyValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < Math.pow(1000, 3)) {
                return (value / Math.pow(1000, 2)).toFixed(3);
            } else if (value < Math.pow(1000, 4)) {
                return (value / Math.pow(1000, 3)).toFixed(3);
            } else if (value < Math.pow(1000, 5)) {
                return (value / Math.pow(1000, 4)).toFixed(3);
            } else {
                return (value / Math.pow(1000, 5)).toFixed(3);
            }
        };
    }
    
    public static unstyleFrequencyValue() {
        return (value: number, unit: string): number => {
            if (value == -1) return value
            if (isNaN(value)) return Number.NaN
            switch (unit.toLowerCase()) {
            case 'm':
            case 'mhz':
                return value * Math.pow(1000, 2)
            case 'g':
            case 'ghz':
                return value * Math.pow(1000, 3)
            case 't':
            case 'thz':
                return value * Math.pow(1000, 4)
            case 'p':
            case 'phz':
                return value * Math.pow(1000, 5)
            default:
                return value
            }
        }
    }
    
    public static styleFrequencyUnitValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < Math.pow(1000, 3)) {
                return FormatUtils.customPrecision(value / Math.pow(1000, 2)) + ' MHz';
            } else if (value < Math.pow(1000, 4)) {
                return FormatUtils.customPrecision(value / Math.pow(1000, 3)) + ' GHz';
            } else if (value < Math.pow(1000, 5)) {
                return FormatUtils.customPrecision(value / Math.pow(1000, 4)) + ' THz';
            } else {
                return FormatUtils.customPrecision(value / Math.pow(1000, 5)) + ' PHz';
            }
        };
    }
    
    // export function unstyleFrequencyUnitValue() {
    //     return (unitValue: string): number => {
    //         if (unitValue == 'unsp') return -1
    //         var value: number = Number.parseFloat(unitValue.replace(/[^0-9\.]+/, ''))
    //         if (isNaN(value)) return Number.NaN
    //         var unit: string = unitValue.replace(/[0-9\.]+/, '').trim()
    //         switch (unit.toLowerCase()) {
    //         case 'mhz':
    //             return value * Math.pow(1000, 2)
    //         case 'ghz':
    //             return value * Math.pow(1000, 3)
    //         case 'thz':
    //             return value * Math.pow(1000, 4)
    //         case 'phz':
    //             return value * Math.pow(1000, 5)
    //         default:
    //             return Number.NaN
    //         }
    //     }
    // }
    
    public static styleDurationUnitValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            if (value < 60) {
                return FormatUtils.customPrecision(value, 2) + ' s';
            } else if (value / 60 < 60) {
                return FormatUtils.customPrecision(value / 60, 2) + ' min';
            } else if (value / 60 / 60 < 24) {
                return FormatUtils.customPrecision(value / 60 / 60, 2) + ' hr';
            } else {
                return FormatUtils.customPrecision(value / 60 / 60 / 24) + ' d';
            }
        };
    }
    
    // export function unstyleDurationUnitValue() {
    //     return (unitValue: string): number => {
    //         if (unitValue == 'unsp') return -1
    //         var value: number = Number.parseFloat(unitValue.replace(/[^0-9\.]+/, ''))
    //         if (isNaN(value)) return Number.NaN
    //         var unit: string = unitValue.replace(/[0-9\.]+/, '').trim()
    //         switch (unit.toLowerCase()) {
    //         case 's':
    //             return value
    //         case 'min':
    //         case 'm':
    //             return value * 60
    //         case 'hr':
    //         case 'h':
    //             return value * 60 * 60
    //         case 'd':
    //             return value * 60 * 60 * 24
    //         default:
    //             return Number.NaN
    //         }
    //     }
    // }
    
    public static styleRatingUnit() {
        return (value: number): string => {
            if (value == -1) return ''
            return '%';
        }
    }
    
    public static styleRatingValue() {
        return (value: number): string => {
            if (value == -1) return 'unsp'
            return (value * 100).toFixed(3);
        }
    }
    
    public static unstyleRatingValue() {
        return (value: number, unit: string): number => {
            if (value == -1) return value
            if (isNaN(value)) return Number.NaN
            return value / 100
        }
    }
    
    // export function styleRatingUnitValue() {
    //     return (value: number): string => {
    //         if (value == -1) return 'unsp'
    //         return FormatUtils.customPrecision(value, 2) + '%';
    //     }
    // }
    
    // export function unstyleRatingUnitValue() {
    //     return (unitValue: string): number => {
    //         if (unitValue == 'unsp') return -1
    //         var value: number = Number.parseFloat(unitValue.replace(/[^0-9\.]+/, ''))
    //         if (isNaN(value)) return Number.NaN
    //         if (unitValue.replace(/[0-9\.%]/g, '') != '') return Number.NaN
    //         return value;
    //     }
    // }
    
    public static styleRateUnit() {
        return (value: number): string => {
            return '$/hr';
        };
    }
    
    public static styleRateValue() {
        return (value: number): string => {
            return value.toString();
        };
    }
    
    public static styleRateUnitValue() {
        return (value: number): string => {
            return '$' + value.toFixed(2) + '/hr';
        };
    }
    
    // export function unstyleRateUnitValue() {
    //     return (unitValue: string): number => {
    //         var value: number = Number.parseFloat(unitValue.replace(/[^0-9\.]/g, ''))
    //         if (isNaN(value)) return Number.NaN
    //         var unit: string = unitValue.replace(/[0-9\.]+/, '').trim()
    //         switch (unit.toLowerCase()) {
    //         case '$/min':
    //             return value * 60;
    //         case '$/hr':
    //             return value * 1;
    //         case '$/day':
    //             return value / 24;
    //         default:
    //             return Number.NaN
    //         }
    //     }
    // }
    
    public static styleRate() {
        return (value: number): string => {
            if (isNaN(value)) {
                return 'no match';
            } else if (value >= 0.1) {
                return '$' + value.toFixed(2) + '/hr';
            } else {
                return (value * 100).toFixed(1) + '¢/hr';
            }
        };
    }
    
    private static customPrecision(value: number, maxPrecision = 3): string {
        var places: number = Math.floor(value).toString().length;
        if (places <= maxPrecision) {
            var ret = value.toPrecision(maxPrecision);
            // Shorten the text if it ends in 0 or .
            while (ret.endsWith('0')) ret = ret.substr(0, ret.length-1);
            if (ret.endsWith('.')) ret = ret.substr(0, ret.length-1);
            return ret;
        } else {
            return value.toString();
        }
    }
}