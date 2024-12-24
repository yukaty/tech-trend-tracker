export default function Footer() {
    return (
      <footer className="text-center py-4 text-sm text-gray-500">
        © {new Date().getFullYear()} <span className="font-medium">Tech Trend Tracker</span>. All rights reserved.
      </footer>
    );
  }
