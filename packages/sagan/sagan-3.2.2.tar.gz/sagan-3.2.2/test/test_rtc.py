from sagan.rtc import _parse_rtc_bytes


def to_bcd(x):
    return ((x // 10) << 4) | (x % 10)


def test_rtc_parse():
    for i in range(100):
        hundredths = i
        sec = i % 60
        min = i % 60
        hour = i % 24
        day = i % 31
        wk_day = i % 7
        mon = i % 12
        year = i

        regs = [
            to_bcd(hundredths),
            0x80 | to_bcd(sec),
            to_bcd(min),
            to_bcd(hour),
            to_bcd(day),
            to_bcd(wk_day),
            to_bcd(mon),
            to_bcd(year)
        ]

        parsed = _parse_rtc_bytes(regs)

        assert parsed.hundredths_of_seconds == hundredths
        assert parsed.second == sec
        assert parsed.minute == min
        assert parsed.hour == hour
        assert parsed.day == day
        assert parsed.week_day == wk_day
        assert parsed.month == mon
        assert parsed.year == year
