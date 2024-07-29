class Board {
    enum State { null, WHITE, BLACK; }
    State get(int x, int y);
    int get_number_of_white();
    int get_number_of_black();
    // throws IllegalStateException if can't play
    Board move(int x, int y);
};

int Area_Index(int x, int y)
{
    int I[8][8] = {
    {0, 1, 2, 2, 2, 2, 1, 0},
    {1, 3, 4, 4, 4, 4, 3, 1},
    {2, 4, 5, 6, 6, 5, 4, 2},
    {2, 4, 6, 7 ,7 ,6 ,4, 2},
    {2, 4, 6, 7, 7, 6, 4, 2},
    {2, 4, 5, 6, 6, 5, 4, 2},
    {1, 3, 4, 4, 4, 4, 3, 1},
    {0, 1, 2, 2, 2, 2, 1, 0}};
    return I[x][y]
}

eval(Board BO, vector<int> constant);

int get_number_of_white()
{
    int number(0);
    for(int i=0; i<8; i++)
    {
        for(int j=0; j<8; j++)
        {
        if(get(i, j) == State::WHITE)
        {
            number++;
        }
    }
    return number;
}

int get_number_of_black()
{
    int number(0);
    for(int i=0; i<8; i++)
    {
        for(int j=0; j<8; j++)
        {
            if(get(i, j) == State::BLACK)
            {
                number++;
            }
        }
    }
    return number;
}
        

get_number_of_black()

eval(Board BO, vector<int> constant, MyColor, YourColor)
{
    int M(64);
    int Eval(0);
    
    for(int i=0; i<8; i++)
    {
        for(int j=0; j<8; j++)
        {
            try
            {
                get(i,j)
            }
            catch(IllegalStateException e) {
                M--;
            }
        }
    }
    
    if(E<12)
    {
        for(int i=0; i<8; i++)
        {
            for(int j=0; j<8; j++)
            {
                if(get(i, j) == MyColor)
                {
                    Eval += constant[Area_Index(i,j)];
                }
                if(get(i, j) == YourColor)
                {
                    Eval -= constant[Area_Index(i,j)];
                }
            }
        }
        Eval += M*constant[8];
    }
    else if(E<20)
    {
        for(int i=0; i<8; i++)
        {
            for(int j=0; j<8; j++)
            {
                if(get(i, j) == MyColor)
                {
                    Eval += constant[Area_Index(i,j)+9];
                }
                if(get(i, j) == YourColor)
                {
                    Eval -= constant[Area_Index(i,j)+9];
                }
            }
        }
        Eval += M*constant[17];
    }
    else if(E<28)
    {
        for(int i=0; i<8; i++)
        {
            for(int j=0; j<8; j++)
            {
                if(get(i, j) == MyColor)
                {
                    Eval += constant[Area_Index(i,j)+18];
                }
                if(get(i, j) == YourColor)
                {
                    Eval -= constant[Area_Index(i,j)+18];
                }
            }
        }
        Eval += M*constant[26];
    }
    else if(E<36)
    {
        for(int i=0; i<8; i++)
        {
            for(int j=0; j<8; j++)
            {
                if(get(i, j) == MyColor)
                {
                    Eval += constant[Area_Index(i,j)+27];
                }
                if(get(i, j) == YourColor)
                {
                    Eval -= constant[Area_Index(i,j)+27];
                }
            }
        }
        Eval += M*constant[35];
    }
    else if(E<44)
    {
        for(int i=0; i<8; i++)
        {
            for(int j=0; j<8; j++)
            {
                if(get(i, j) == MyColor)
                {
                    Eval += constant[Area_Index(i,j)+36];
                }
                if(get(i, j) == YourColor)
                {
                    Eval -= constant[Area_Index(i,j)+36];
                }
            }
        }
        Eval += M*constant[44];
    }
    else if(E<52)
    {
        for(int i=0; i<8; i++)
        {
            for(int j=0; j<8; j++)
            {
                if(get(i, j) == MyColor)
                {
                    Eval += constant[Area_Index(i,j)+45];
                }
                if(get(i, j) == YourColor)
                {
                    Eval -= constant[Area_Index(i,j)+45];
                }
            }
        }
        Eval += M*constant[53];
    }
    else
    {
        for(int i=0; i<8; i++)
        {
            for(int j=0; j<8; j++)
            {
                if(get(i, j) == MyColor)
                {
                    Eval += constant[Area_Index(i,j)+54];
                }
                if(get(i, j) == YourColor)
                {
                    Eval -= constant[Area_Index(i,j)+54];
                }
            }
        }
        Eval += M*constant[62];
    }
}
