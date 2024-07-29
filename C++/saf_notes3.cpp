#include <vector>
#include <utility>
#include <algorithm>
#include <iostream>
#include <string>
#include <istream>
#include <ostream>
#include <cassert>
#include <stdexcept>
#include <climits>
#include <ctime>

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
  mutable std::vector<std::pair<int, int> > next_;
  mutable bool next_valid;
  mutable int eval;
  mutable bool eval_valid;
  friend int evaluate(board const&);
public:
  state turn() const { return turn_; }
  board():
    pieces(initial()), turn_(black), next_valid(false), eval_valid(false) {}
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
  std::pair<int, int> last_move() const { return last_move_; }
  std::vector<std::pair<int, int> > const& next() const {
    if(!next_valid) {
      next_.clear();
      FOR_BOARD(i, j) {
        std::pair<bool, board> p=play(i, j);
        if(p.first) next_.push_back(std::pair<int, int>(i, j));
      }
    }
    return next_;
  }
  bool end() const { return next().empty(); }
  std::pair<bool, board> play(int x, int y) const {
    board b(*this);
    b.turn_ = (turn() == white ? black : white);
    b.last_move_ = std::pair<int, int>(x, y);
    bool valid=false;
    if(b(x, y)==empty) {
      b(x, y)=turn();
      FOR_DIRECTION(i, j) {
        for(int xx=x+i, yy=y+j; valid_index(xx) && valid_index(yy); xx+=i, yy+=j)
          if(b(xx, yy)==empty) break;
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

int evaluate(board const& b) {
  if(b.eval_valid) return b.eval;
  int& i=b.eval;
  i=0;
  for(int x=1; x<board::size-1; ++x) for(int y=1; y<board::size-1; ++y) {
    if(b(x, y)==board::white) i++;
    if(b(x, y)==board::black) i--;
  }
  int const side_advantage = 5;
  for(int x=1; x<board::size-1; ++x) {
    if(b(x, 0)==board::white) i+=side_advantage;
    if(b(x, 0)==board::black) i-=side_advantage;
    if(b(x, board::size-1)==board::white) i+=side_advantage;
    if(b(x, board::size-1)==board::black) i-=side_advantage;
    if(b(0, x)==board::white) i+=side_advantage;
    if(b(0, x)==board::black) i-=side_advantage;
    if(b(board::size-1, x)==board::white) i+=side_advantage;
    if(b(board::size-1, x)==board::black) i-=side_advantage;
  }
  int const corner_advantage = 50;
  if(b(0, 0)==board::white) i+=corner_advantage;
  if(b(0, 0)==board::black) i-=corner_advantage;
  if(b(0, board::size-1)==board::white) i+=corner_advantage;
  if(b(0, board::size-1)==board::black) i-=corner_advantage;
  if(b(board::size-1, 0)==board::white) i+=corner_advantage;
  if(b(board::size-1, 0)==board::black) i-=corner_advantage;
  if(b(board::size-1, board::size-1)==board::white) i+=corner_advantage;
  if(b(board::size-1, board::size-1)==board::black) i-=corner_advantage;
  return i;
}


int search(board const& b, int depth, int alpha, int beta) {
  if(b.end() || !depth) return evaluate(b);
  std::vector<std::pair<int, int> > const n(b.next());
  for(std::vector<std::pair<int, int> >::const_iterator i=n.begin(); i!=n.end(); ++i) {
    alpha = std::max(alpha, -search(b.play(i->first, i->second).second, depth-1, -beta, -alpha));
    if(alpha>=beta) return alpha;
  }
  return alpha;
}

std::pair<int, int> best(board const& b) {/*
  int i=0;
  FOR_BOARD(x, y) {
    if(b.play(x, y).first) ++i;
  }*/
  int const depth = 8; // no of recursions

  if(b.end()) return std::pair<int, int>(-1, -1);
  std::vector<std::pair<int, int> > const n(b.next());
  std::pair<int, int> p = std::pair<int, int>(-1, -1); // pass
  int a = INT_MIN;
  for(std::vector<std::pair<int, int> >::const_iterator i=n.begin(); i!=n.end(); ++i) {
    int s = search(b.play(i->first, i->second).second, depth, INT_MIN, INT_MAX);
    std::cerr<<"pair ("<<i->first+1<<", "<<i->second+1<<") is "<<s<<std::endl;
    if(s>a) {
      p=*i;
      a=s;
    }
  }
  return p;
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
    std::time_t t1 = std::time(NULL);
    std::pair<int, int> n(best(b));
    std::cerr<<"It took "<<std::difftime(std::time(NULL), t1)<<" s.\n";
    std::cout<<"Lo and behold! For I shall play at ("<<n.first+1<<", "<<n.second+1<<")!\n";
    assert(b.play(n.first, n.second).first);
    b=b.play(n.first, n.second).second;
    std::cout<<"Current evaluation: "<<evaluate(b)<<std::endl;
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
