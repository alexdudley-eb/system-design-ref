import { render, screen, waitFor, act } from "@testing-library/react";
import QuizTimer from "@/components/QuizTimer";
import { saveTimerState, clearTimerState } from "@/lib/quizStorage";

jest.useFakeTimers();

describe("QuizTimer", () => {
  beforeEach(() => {
    localStorage.clear();
    jest.clearAllTimers();
  });

  afterEach(() => {
    jest.clearAllTimers();
  });

  it("renders with initial time formatted correctly", () => {
    const onTimeUp = jest.fn();
    const onTick = jest.fn();

    render(
      <QuizTimer
        sessionId="test-1"
        totalSeconds={3600}
        onTimeUp={onTimeUp}
        onTick={onTick}
      />,
    );

    expect(screen.getByText(/60:00/)).toBeInTheDocument();
  });

  it("formats time correctly for various durations", () => {
    const testCases = [
      { seconds: 3600, expected: "60:00" },
      { seconds: 1800, expected: "30:00" },
      { seconds: 90, expected: "01:30" },
      { seconds: 45, expected: "00:45" },
    ];

    testCases.forEach(({ seconds, expected }) => {
      const { unmount } = render(
        <QuizTimer
          sessionId={`test-${seconds}`}
          totalSeconds={seconds}
          onTimeUp={jest.fn()}
          onTick={jest.fn()}
        />,
      );

      expect(screen.getByText(expected)).toBeInTheDocument();
      unmount();
    });
  });

  it("counts down every second", async () => {
    const onTimeUp = jest.fn();
    const onTick = jest.fn();

    render(
      <QuizTimer
        sessionId="test-2"
        totalSeconds={10}
        onTimeUp={onTimeUp}
        onTick={onTick}
      />,
    );

    expect(screen.getByText("00:10")).toBeInTheDocument();

    await act(async () => {
      jest.advanceTimersByTime(1000);
    });

    await waitFor(() => {
      expect(onTick).toHaveBeenCalled();
    });
  });

  it("calls onTimeUp when timer reaches zero", async () => {
    const onTimeUp = jest.fn();
    const onTick = jest.fn();

    render(
      <QuizTimer
        sessionId="test-3"
        totalSeconds={2}
        onTimeUp={onTimeUp}
        onTick={onTick}
      />,
    );

    await act(async () => {
      jest.advanceTimersByTime(3000);
    });

    await waitFor(
      () => {
        expect(onTimeUp).toHaveBeenCalled();
      },
      { timeout: 1000 },
    );
  });

  it("saves timer start time to localStorage", () => {
    const onTimeUp = jest.fn();
    const onTick = jest.fn();
    const sessionId = "test-4";

    render(
      <QuizTimer
        sessionId={sessionId}
        totalSeconds={30}
        onTimeUp={onTimeUp}
        onTick={onTick}
      />,
    );

    const stored = localStorage.getItem(`timer_${sessionId}`);
    expect(stored).not.toBeNull();
  });

  it("restores timer state on remount", () => {
    const sessionId = "test-5";
    const startTime = Date.now() - 5000;
    saveTimerState(sessionId, startTime);

    const { unmount } = render(
      <QuizTimer
        sessionId={sessionId}
        totalSeconds={30}
        onTimeUp={jest.fn()}
        onTick={jest.fn()}
      />,
    );

    const timerText = screen.getByText(/00:2[45]/);
    expect(timerText).toBeInTheDocument();

    unmount();
  });

  it("handles timer expiration correctly", async () => {
    const sessionId = "test-6";
    const startTime = Date.now() - 31000;
    saveTimerState(sessionId, startTime);

    const onTimeUp = jest.fn();
    const onTick = jest.fn();

    render(
      <QuizTimer
        sessionId={sessionId}
        totalSeconds={30}
        onTimeUp={onTimeUp}
        onTick={onTick}
      />,
    );

    expect(screen.getByText("00:00")).toBeInTheDocument();
  });

  it("pauses timer on document visibility change", async () => {
    const onTimeUp = jest.fn();
    const onTick = jest.fn();

    render(
      <QuizTimer
        sessionId="test-7"
        totalSeconds={60}
        onTimeUp={onTimeUp}
        onTick={onTick}
      />,
    );

    await act(async () => {
      jest.advanceTimersByTime(2000);
    });

    const callCountBeforePause = onTick.mock.calls.length;

    await act(async () => {
      Object.defineProperty(document, "hidden", {
        writable: true,
        value: true,
      });
      document.dispatchEvent(new Event("visibilitychange"));
    });

    await act(async () => {
      jest.advanceTimersByTime(5000);
    });

    const callCountWhileHidden = onTick.mock.calls.length;

    expect(callCountWhileHidden).toBeLessThanOrEqual(callCountBeforePause + 1);

    await act(async () => {
      Object.defineProperty(document, "hidden", {
        writable: true,
        value: false,
      });
      document.dispatchEvent(new Event("visibilitychange"));
    });

    await act(async () => {
      jest.advanceTimersByTime(2000);
    });

    expect(onTick.mock.calls.length).toBeGreaterThan(callCountWhileHidden);
  });

  it("properly cleans up timer on unmount", async () => {
    const onTimeUp = jest.fn();
    const onTick = jest.fn();

    const { unmount } = render(
      <QuizTimer
        sessionId="test-8"
        totalSeconds={60}
        onTimeUp={onTimeUp}
        onTick={onTick}
      />,
    );

    const callsBeforeUnmount = onTick.mock.calls.length;

    unmount();

    await act(async () => {
      jest.advanceTimersByTime(5000);
    });

    expect(onTick.mock.calls.length).toBe(callsBeforeUnmount);
  });

  it("handles multiple remounts correctly", async () => {
    const sessionId = "test-9";
    const onTimeUp = jest.fn();
    const onTick = jest.fn();

    const { unmount: unmount1 } = render(
      <QuizTimer
        sessionId={sessionId}
        totalSeconds={60}
        onTimeUp={onTimeUp}
        onTick={onTick}
      />,
    );

    await act(async () => {
      jest.advanceTimersByTime(2000);
    });
    unmount1();

    const { unmount: unmount2 } = render(
      <QuizTimer
        sessionId={sessionId}
        totalSeconds={60}
        onTimeUp={onTimeUp}
        onTick={onTick}
      />,
    );

    await act(async () => {
      jest.advanceTimersByTime(2000);
    });
    unmount2();

    const { unmount: unmount3 } = render(
      <QuizTimer
        sessionId={sessionId}
        totalSeconds={60}
        onTimeUp={onTimeUp}
        onTick={onTick}
      />,
    );

    expect(screen.getByText(/00:5[0-9]/)).toBeInTheDocument();
    unmount3();
  });
});
