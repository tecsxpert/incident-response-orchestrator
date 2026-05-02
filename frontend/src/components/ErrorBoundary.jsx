import {Component} from "react";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    console.log("Error caught:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-6 text-center">
          <p className="text-xl font-semibold text-gray-700 mb-2">Something went wrong.</p>
          <p className="text-sm text-gray-400 mb-4">Please refresh the page or try again later.</p>
          <button
            onClick={() => this.setState({ hasError: false })}
            className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded text-sm">
            Try Again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}