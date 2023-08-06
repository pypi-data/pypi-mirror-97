/*
 * Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package monasca.common.util;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.regex.Pattern;

import javax.annotation.concurrent.Immutable;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonAutoDetect.Visibility;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.databind.ser.std.ToStringSerializer;
import com.google.common.base.Preconditions;

/**
 * Duration unit, consisting of length and time unit.
 */
@Immutable
@JsonAutoDetect(fieldVisibility = Visibility.ANY, getterVisibility = Visibility.NONE,
    isGetterVisibility = Visibility.NONE)
@JsonSerialize(using = ToStringSerializer.class)
public class Duration implements Serializable {
  private static final long serialVersionUID = -2047960773448166416L;
  /** A duration of Long.MAX_VALUE Days */
  public static final Duration INFINITE = new Duration();
  static final Pattern PATTERN = Pattern.compile("[\\d]+[\\s]*(" + "ns|nanosecond(s)?|"
      + "us|microsecond(s)?|" + "ms|millisecond(s)?|" + "s|second(s)?|" + "m|minute(s)?|"
      + "h|hour(s)?|" + "d|day(s)?" + ')');
  private static final Map<String, TimeUnit> SUFFIXES;

  public final long length;
  public final TimeUnit timeUnit;
  public final boolean finite;

  static {
    SUFFIXES = new HashMap<String, TimeUnit>();

    SUFFIXES.put("ns", TimeUnit.NANOSECONDS);
    SUFFIXES.put("nanosecond", TimeUnit.NANOSECONDS);
    SUFFIXES.put("nanoseconds", TimeUnit.NANOSECONDS);

    SUFFIXES.put("us", TimeUnit.MICROSECONDS);
    SUFFIXES.put("microsecond", TimeUnit.MICROSECONDS);
    SUFFIXES.put("microseconds", TimeUnit.MICROSECONDS);

    SUFFIXES.put("ms", TimeUnit.MILLISECONDS);
    SUFFIXES.put("millisecond", TimeUnit.MILLISECONDS);
    SUFFIXES.put("milliseconds", TimeUnit.MILLISECONDS);

    SUFFIXES.put("s", TimeUnit.SECONDS);
    SUFFIXES.put("second", TimeUnit.SECONDS);
    SUFFIXES.put("seconds", TimeUnit.SECONDS);

    SUFFIXES.put("m", TimeUnit.MINUTES);
    SUFFIXES.put("minute", TimeUnit.MINUTES);
    SUFFIXES.put("minutes", TimeUnit.MINUTES);

    SUFFIXES.put("h", TimeUnit.HOURS);
    SUFFIXES.put("hour", TimeUnit.HOURS);
    SUFFIXES.put("hours", TimeUnit.HOURS);

    SUFFIXES.put("d", TimeUnit.DAYS);
    SUFFIXES.put("day", TimeUnit.DAYS);
    SUFFIXES.put("days", TimeUnit.DAYS);
  }

  /** Infinite constructor. */
  private Duration() {
    finite = false;
    this.length = Long.MAX_VALUE;
    this.timeUnit = TimeUnit.DAYS;
  }

  private Duration(long length, TimeUnit timeUnit) {
    this.length = length;
    this.timeUnit = Preconditions.checkNotNull(timeUnit);
    finite = length == Long.MAX_VALUE && TimeUnit.DAYS.equals(timeUnit) ? false : true;
  }

  public static Duration days(long count) {
    return new Duration(count, TimeUnit.DAYS);
  }

  public static Duration hours(long count) {
    return new Duration(count, TimeUnit.HOURS);
  }

  public static Duration inf() {
    return INFINITE;
  }

  public static Duration infinite() {
    return INFINITE;
  }

  public static Duration microseconds(long count) {
    return new Duration(count, TimeUnit.MICROSECONDS);
  }

  public static Duration millis(long count) {
    return new Duration(count, TimeUnit.MILLISECONDS);
  }

  public static Duration milliseconds(long count) {
    return new Duration(count, TimeUnit.MILLISECONDS);
  }

  public static Duration mins(long count) {
    return new Duration(count, TimeUnit.MINUTES);
  }

  public static Duration minutes(long count) {
    return new Duration(count, TimeUnit.MINUTES);
  }

  public static Duration nanos(long count) {
    return new Duration(count, TimeUnit.NANOSECONDS);
  }

  public static Duration nanoseconds(long count) {
    return new Duration(count, TimeUnit.NANOSECONDS);
  }

  public static Duration of(long count, TimeUnit unit) {
    return new Duration(count, unit);
  }

  @JsonCreator
  public static Duration of(String duration) {
    Preconditions.checkArgument(PATTERN.matcher(duration).matches(), "Invalid duration: %s",
        duration);
    int i = 0;
    for (; i < duration.length(); i++)
      if (Character.isLetter(duration.charAt(i)))
        break;
    String unit = duration.subSequence(0, i).toString().trim();
    String dur = duration.subSequence(i, duration.length()).toString();
    return new Duration(Long.parseLong(unit), SUFFIXES.get(dur));
  }

  public static Duration seconds(long count) {
    return new Duration(count, TimeUnit.SECONDS);
  }

  public static Duration secs(long count) {
    return new Duration(count, TimeUnit.SECONDS);
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj)
      return true;
    if ((obj == null) || (getClass() != obj.getClass()))
      return false;
    final Duration duration = (Duration) obj;
    return (length == duration.length) && (timeUnit == duration.timeUnit);
  }

  @Override
  public int hashCode() {
    return (31 * (int) (length ^ (length >>> 32))) + timeUnit.hashCode();
  }

  public long toDays() {
    return TimeUnit.DAYS.convert(length, timeUnit);
  }

  public long toHours() {
    return TimeUnit.HOURS.convert(length, timeUnit);
  }

  public long toMicros() {
    return TimeUnit.MICROSECONDS.convert(length, timeUnit);
  }

  public long toMicroseconds() {
    return TimeUnit.MICROSECONDS.convert(length, timeUnit);
  }

  public long toMillis() {
    return TimeUnit.MILLISECONDS.convert(length, timeUnit);
  }

  public long toMilliseconds() {
    return TimeUnit.MILLISECONDS.convert(length, timeUnit);
  }

  public long toMins() {
    return TimeUnit.MINUTES.convert(length, timeUnit);
  }

  public long toMinutes() {
    return TimeUnit.MINUTES.convert(length, timeUnit);
  }

  public long toNanos() {
    return TimeUnit.NANOSECONDS.convert(length, timeUnit);
  }

  public long toNanoseconds() {
    return TimeUnit.NANOSECONDS.convert(length, timeUnit);
  }

  public long toSeconds() {
    return TimeUnit.SECONDS.convert(length, timeUnit);
  }

  public long toSecs() {
    return TimeUnit.SECONDS.convert(length, timeUnit);
  }

  @Override
  public String toString() {
    String units = timeUnit.toString().toLowerCase();
    if (length == 1)
      units = units.substring(0, units.length() - 1);
    return Long.toString(length) + ' ' + units;
  }
}
