#include <vector>
#include <utility>
#include <algorithm>
#include <iostream>
#include <string>
#include <istream>
#include <ostream>
#include <cassert>
#include <stdexcept>

#define FOR_BOARD(x, y) for(int x=0; x<board::size; ++x)\
                          for(int y=0; y<board::size; ++y)
#define FOR_DIRECTION(x, y) for(int x=-1; x<2; ++x)\
                              for(int y=-1; y<2; ++y)\
                                if(x==0&&y==0); else
class board {
public:
  enum state {empty, white, black};
  static int const size = 010;
private:
  std::vector<std::vector<state> > pieces;
  state turn_;
  std::pair<int, int> last_move_;
  bool valid_index(int i) const { return i>=0 && i<board::size; }
  static std::vector<std::vector<state> > initial() {
    std::vector<std::vector<state> > v=
      std::vector<std::vector<state> >(8, std::vector<state>(8, empty));
    v[3][3]=v[4][4]=white;
    v[4][3]=v[3][4]=black;
    return v;
  }
  friend bool operator==(board const&, board const&);
public:
  state turn() const { return turn_; }
  board():
    pieces(initial()),
    turn_(black) {}
  state& operator()(int x, int y) {
    if(!valid_index(x) || !valid_index(y))
      throw std::out_of_range("invalid indices");
    return pieces[x][y];
  }
  state const& operator()(int x, int y) const {
    if(!valid_index(x) || !valid_index(y))
      throw std::out_of_range("invalid indices");
    return pieces[x][y];
  }
  std::pair<int, int> last_move() { return last_move_; }
  std::vector<board> next() const {
    std::vector<board> v;
    FOR_BOARD(i, j) {
      std::pair<bool, board> p=play(i, j);
      if(p.first) v.push_back(p.second); 
    }
    return v;
  }
  bool end() { return next().empty(); }
  std::pair<bool, board> play(int x, int y) const {
    board b(*this);
    b.turn_ = (turn() == white ? black : white);
    b.last_move_ = std::pair<int, int>(x, y);
    bool valid=false;
    if(b(x, y)==empty) {
      b(x, y)=turn();
      FOR_DIRECTION(i, j) {
        for(int xx=x+i, yy=y+j; valid_index(xx) && valid_index(yy); xx+=i, yy+=j)
          if(b(xx, yy)==empty) { 
            break;}
          else if(b(xx, yy)==turn()) {
            if(xx!=x+i||yy!=y+j) {
              for(int xxx=x+i, yyy=y+j; xxx!=xx || yyy!=yy; xxx+=i, yyy+=j)
                b(xxx, yyy) = turn();
              valid=true;
            }
            break;
          }
      }
    }
    return std::pair<bool, board>(valid, b);
  }
};

bool operator==(board const& b1, board const& b2) {
  return b1.pieces==b2.pieces && b1.turn_==b2.turn_ && b1.last_move_==b2.last_move_;
}


// compares how much the board is advantageous to the current turn.
int evaluate(board const& b) {
  int i=0;
  for(int x=1; x<board::size-1; ++x) for(int y=1; y<board::size-1; ++y) {
    if(b(x, y)==b.turn()) i++;
    if(b(x, y)==(b.turn()==board::white ? board::black : board::white)) i--;
  }
  int const side_advantage = 5;
  for(int x=1; x<board::size-1; ++x) {
    if(b(x, 0)==b.turn()) i+=side_advantage;
    if(b(x, 0)==(b.turn()==board::white ? board::black : board::white)) i-=side_advantage;
    if(b(x, board::size-1)==b.turn()) i+=side_advantage;
    if(b(x, board::size-1)==(b.turn()==board::white ? board::black : board::white)) i-=side_advantage;
    if(b(0, x)==b.turn()) i+=side_advantage;
    if(b(0, x)==(b.turn()==board::white ? board::black : board::white)) i-=side_advantage;
    if(b(board::size-1, x)==b.turn()) i+=side_advantage;
    if(b(board::size-1, x)==(b.turn()==board::white ? board::black : board::white)) i-=side_advantage;
  }
  int const corner_advantage = 50;
  if(b(0, 0)==b.turn()) i+=corner_advantage;
  if(b(0, 0)==(b.turn()==board::white ? board::black : board::white)) i-=corner_advantage;
  if(b(0, board::size-1)==b.turn()) i+=corner_advantage;
  if(b(0, board::size-1)==(b.turn()==board::white ? board::black : board::white)) i-=corner_advantage;
  if(b(board::size-1, 0)==b.turn()) i+=corner_advantage;
  if(b(board::size-1, 0)==(b.turn()==board::white ? board::black : board::white)) i-=corner_advantage;
  if(b(board::size-1, board::size-1)==b.turn()) i+=corner_advantage;
  if(b(board::size-1, board::size-1)==(b.turn()==board::white ? board::black : board::white)) i-=corner_advantage;
  return i;
}

bool compare(std::pair<board, board> const& p1, std::pair<board, board> const& p2) {
  return evaluate(p1.second)<evaluate(p2.second);
}

std::vector<std::pair<board, board> > combine(board const&, int);

board search(board b, int depth) {
  std::vector<std::pair<board, board> > v=combine(b, depth);
  return std::max_element(v.begin(), v.end(), compare)->first;
}

std::vector<std::pair<board, board> > combine(board const& b, int depth) {
  std::vector<std::pair<board, board> > v;
  std::vector<board> const next(b.next());
  for(std::vector<board>::const_iterator i=next.begin(); i!=next.end(); ++i) {
    if(depth) {
      std::vector<std::pair<board, board> > const w=combine(search(*i, depth-1), depth-1);
      for(std::vector<std::pair<board, board> >::const_iterator j=w.begin(); j!=w.end(); ++j)
        v.push_back(std::pair<board, board>(*i, j->second));
    } else v.push_back(std::pair<board, board>(*i, *i));
  }
  return v;
}


std::pair<int, int> best_move(board b) {
  int i=0;
  FOR_BOARD(x, y) {
    if(b.play(x, y).first) ++i;
  }
  int const depth = i; // arbitrary value; make adjustable
  board best=search(b, depth);
  FOR_BOARD(x, y)
    if(best(x, y)!=board::empty && b(x, y)==board::empty)
      return std::pair<int, int>(x, y);
  assert(false); // or should pass
}



board::state winner(board const& b) {
  int i=0;
  FOR_BOARD(x, y)
    switch(b(x, y)) {
      case board::white: i++; break;
      case board::black: i--; break;
      default: break;
    }
  return i>0 ? board::white : i<0 ? board::black : board::empty;
}


template <typename Elem, typename Tr>
std::basic_ostream<Elem, Tr>& operator<<(std::basic_ostream<Elem, Tr>& s, board const& b) {
  for(int i=0; i<board::size; ++i) {
    for(int j=0; j<board::size; ++j) {
      switch(b(i, j)) {
      case board::empty:
        s<<std::basic_string<Elem, Tr>(1,'_');
        break;
      case board::white:
        s<<std::basic_string<Elem, Tr>(1,'O');
        break;
      case board::black:
        s<<std::basic_string<Elem, Tr>(1,'#');
        break;
      }
      s<<std::basic_string<Elem, Tr>(1,' ');
    }
    s<<std::endl;
  }
  return s;
}

int main() {
  std::cout<<"Welcome, stranger, to Messrs Kim, Kweon & Lee's "
             "fantasmagorical hall of Othello!\n"
             "Darest thou challenge me, the AI of AIs?\n";
  std::cout<<"Remember, thou art dark!\n";
  
  board b;
  while(true) {
    std::cout<<b;
    std::cout<<"Challenger, move if thou darest: ";
    int x, y;
    std::cin>>x>>y;
    std::pair<bool, board> p(b.play(x-1,y-1));
    if(p.first) b=p.second; else {
       std::cout<<"Fool! Thy moves are foetid!\n";
       continue;
    }
    if(b.end()) break;
    std::cout<<b;
    std::pair<int, int> n(best_move(b));
    std::cout<<"Lo and behold! For I shall play at ("<<n.first+1<<", "<<n.second+1<<")!\n";
    assert(b.play(n.first, n.second).first);
    b=b.play(n.first, n.second).second;
    if(b.end()) break;
  }
  std::cout<<b;
  switch(winner(b)) {
    case board::black:
      std::cout<<"Curses be damned! Thou hast won, but not for long...\n";
      break;
    case board::white:
      std::cout<<"Alleluia! I have bested thee!\n";
      break;
    case board::empty:
      std::cout<<"Alas, 'tis a tie, but not for long...\n";
  }
}
