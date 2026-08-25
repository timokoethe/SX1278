# API Reference

The `sx1278` module exposes the `Lora` class for configuring an SX1278 radio,
sending packets, and receiving packets through the module's DIO0 interrupt.

```python
from sx1278 import Lora
```

## `Lora`

### Constructor

```python
Lora(spi, *, cs, rx, rs, frequency=433.1, bandwidth=250000,
     spreading_factor=10, coding_rate=5, preamble_length=4,
     crc=False, tx_power=17, implicit=False, sync_word=0x12,
     on_recv=None, tx_timeout_ms=5000)
```

Creates and initializes a radio. The constructor resets the module, verifies
that the SX1278 version register contains the expected value, applies the radio
configuration, and leaves the module in standby mode.

| Parameter | Description |
| --- | --- |
| `spi` | Initialized MicroPython `machine.SPI` instance connected to the module. |
| `cs` | Output `machine.Pin` connected to NSS/chip select. |
| `rx` | Input `machine.Pin` connected to DIO0. It is used for receive interrupts. |
| `rs` | Output `machine.Pin` connected to reset. |
| `frequency` | Radio frequency in MHz. Defaults to `433.1`. Select a frequency that is legal in your region. |
| `bandwidth` | Signal bandwidth in Hz. Defaults to `250000`. See [`set_bandwidth()`](#set_bandwidthbw). |
| `spreading_factor` | Spreading factor from `6` through `12`. Defaults to `10`. |
| `coding_rate` | Coding-rate denominator from `5` through `8`, representing `4/5` through `4/8`. Defaults to `5`. |
| `preamble_length` | Preamble length in symbols. Defaults to `4`. |
| `crc` | Enables payload CRC when true. Defaults to `False`. |
| `tx_power` | Transmit power in dBm. Defaults to `17`; the default PA_BOOST path clamps it to `2` through `17` dBm. |
| `implicit` | Enables implicit-header mode when true. Defaults to `False`. |
| `sync_word` | One-byte LoRa sync word. Defaults to `0x12`. |
| `on_recv` | Optional initial receive callback reference. This does not register the DIO0 interrupt; call `on_recv()` before receiving. |
| `tx_timeout_ms` | Maximum time in milliseconds for a transmission to finish. Defaults to `5000`. |

The constructor raises `Exception` if the version register cannot be read as
`0x12`. This normally indicates an SPI, power, reset, or wiring problem.

All communicating radios must use compatible frequency, bandwidth, spreading
factor, header mode, and sync-word settings. In explicit-header mode, coding
rate and CRC presence are included in the packet header. In implicit-header
mode, payload length, coding rate, and CRC must be configured identically on
both radios.

### `send(x)`

```python
lr.send("Hello")
lr.send(b"\x01\x02\x03")
```

Sends one packet. Strings are encoded to bytes using MicroPython's default
encoding. Byte sequences are sent unchanged.

Transmission is blocking. The method returns after the packet has been sent,
or raises `TimeoutError` when `tx_timeout_ms` is exceeded. A packet can contain
at most 255 bytes; a larger packet raises `ValueError`.

### `on_recv(callback)`

```python
def handle_packet(message):
    print(message)

lr.on_recv(handle_packet)
```

Registers a function that receives each valid packet as a `bytes` object. The
callback is invoked from the DIO0 pin's interrupt handler, so it should finish
quickly. The radio remains in continuous receive mode after processing a packet,
so the callback does not normally need to call `recv()` again. Call `recv()` to
resume reception if the callback changes the operating mode, for example by
sending a response or calling `standby()` or `sleep()`.

Pass `None` to remove the callback and disable the DIO0 interrupt:

```python
lr.on_recv(None)
```

Packets with a payload CRC error are discarded without invoking the callback.

### `recv()`

```python
lr.on_recv(handle_packet)
lr.recv()
```

Places the radio in continuous receive mode. Packet delivery requires a receive
callback registered with `on_recv()` and DIO0 connected to the `rx` pin supplied
to the constructor.

### `get_rssi()`

```python
rssi = lr.get_rssi()
```

Returns the received signal strength of the most recently received packet in
dBm.

### `get_snr()`

```python
snr = lr.get_snr()
```

Returns the signal-to-noise ratio of the most recently received packet in dB,
in steps of `0.25` dB.

## Radio configuration

Configuration methods take effect immediately. Configure both ends of a link
with compatible values.

### `set_frequency(frequency)`

Sets the carrier frequency in MHz.

```python
lr.set_frequency(433.1)
```

The driver does not enforce regional frequency limits. Verify the permitted
frequency and operating conditions for your location before transmitting.

### `set_tx_power(level, output_pin=PA_OUTPUT_PA_BOOST_PIN)`

Sets transmit power in dBm.

The default `PA_OUTPUT_PA_BOOST_PIN` path clamps `level` to `2` through `17` dBm.
When `PA_OUTPUT_RFO_PIN` is selected, it clamps `level` to `0` through `14` dBm.
The Ra-01 module normally uses PA_BOOST.

```python
from sx1278 import PA_OUTPUT_RFO_PIN

lr.set_tx_power(14)
lr.set_tx_power(10, PA_OUTPUT_RFO_PIN)
```

### `set_bandwidth(bw)`

Sets signal bandwidth in Hz. The requested value is rounded up to the next
bandwidth supported by the driver:

`7800`, `10400`, `15600`, `20800`, `31250`, `41700`, `62500`, `125000`, or
`250000` Hz. Values above `250000` select `500000` Hz.

```python
lr.set_bandwidth(125000)
```

When changing both bandwidth and spreading factor, set the bandwidth first and
then call `set_spreading_factor()` so low-data-rate optimization is recalculated.

### `set_spreading_factor(sf)`

Sets the spreading factor to an integer from `6` through `12`. Values outside
this range raise `ValueError`.

```python
lr.set_spreading_factor(10)
```

Spreading factor `6` requires implicit-header mode. The driver does not enable
implicit-header mode automatically, so call `set_implicit(True)` explicitly.
Also note the receive limitation described under [`set_implicit()`](#set_implicitimplicitfalse).

### `set_coding_rate(denom)`

Sets the coding rate to `4/denom`. The denominator is clamped to the range `5`
through `8`.

```python
lr.set_coding_rate(5)  # 4/5
```

### `set_preamble_length(n)`

Sets the preamble length in symbols.

```python
lr.set_preamble_length(8)
```

### `set_crc(crc=False)`

Enables or disables payload CRC.

```python
lr.set_crc(True)
```

### `set_sync_word(sw)`

Sets the one-byte LoRa sync word.

```python
lr.set_sync_word(0x12)
```

Radios using different sync words will not communicate.

### `set_implicit(implicit=False)`

Enables or disables implicit-header mode. Both sender and receiver must use the
same header mode. In implicit-header mode, both radios must also use the same
fixed payload length, coding rate, and CRC setting.

```python
lr.set_implicit(True)
```

The current public API does not provide a way to configure the expected fixed
payload length on a receiver. Implicit-header reception, including reception
with spreading factor `6`, is therefore not fully supported. Use explicit-header
mode for receiving unless the driver is extended to configure the receive
payload length.

## Operating modes

### `standby()`

Places the radio in standby mode.

### `sleep()`

Places the radio in sleep mode.

### `reset()`

Performs a hardware reset using the reset pin supplied as `rs`.

## Manual packet construction

Most applications should use `send()`. The following methods expose the same
three transmission steps when a packet needs to be assembled manually:

```python
lr.begin_packet()
lr.write_packet(b"first ")
lr.write_packet(b"second")
lr.end_packet()
```

### `begin_packet()`

Enters standby mode, resets the transmit FIFO pointer, and clears the current
payload length.

### `write_packet(b)`

Appends a byte sequence to the current packet. It raises `ValueError` if the
result would exceed the 255-byte maximum payload length.

### `end_packet()`

Starts transmission and blocks until it completes. It raises `TimeoutError` if
the configured transmit timeout is exceeded.
