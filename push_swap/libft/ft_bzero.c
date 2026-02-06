/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_bzero.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/09 19:54:48 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/09 20:27:02 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
//#include <stdio.h>
//#include <string.h>
//#include <stddef.h>

void	ft_bzero(void *s, size_t n)
{
	ft_memset(s, 0, n);
}

/*int	main(void)
{
	char buffer[50];
    for (int i = 0; i < 50; i++) {
        buffer[i] = (char)('A' + (i % 26));
    }
    printf("Buffer before bzero: %s\n", buffer);
    ft_bzero(buffer, 48);
    printf("Buffer after bzero: %c\n", buffer[49]);
}*/
