package stores

class TestStore extends Store {
  def reset(): Unit = {
    // Nop for now, since the store is read-only
  }
}
